# Define the AWS provider configuration.
provider "aws" {
  region = "us-east-1"  # AWS region.
}

variable "cidr" {
  default = "10.0.0.0/16" #CIDR block for VPC creation.
}

#resource "aws_key_pair" "example" {
#  key_name   = "terraform-HPL-auction"  # desired key name
#  public_key = file("~/.ssh/id_rsa.pub")  # path to the public key file
#}

resource "aws_vpc" "myvpc" {
  cidr_block = var.cidr
}

#subnet creation
resource "aws_subnet" "sub1" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

#Internet gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.myvpc.id
}

#route table creation
resource "aws_route_table" "RT" {
  vpc_id = aws_vpc.myvpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

#associate route table to subnet to make it public

resource "aws_route_table_association" "rta1" {
  subnet_id      = aws_subnet.sub1.id
  route_table_id = aws_route_table.RT.id
}

resource "aws_security_group" "webSg" {
  name   = "web"
  vpc_id = aws_vpc.myvpc.id

  ingress {
    description = "HTTP from VPC"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Web-sg"
  }
}

resource "aws_instance" "HPL-auction-server" {
  ami                    = "ami-053b0d53c279acc90"
  instance_type          = "t2.micro"
  key_name      = "aws-login"
  vpc_security_group_ids = [aws_security_group.webSg.id]
  subnet_id              = aws_subnet.sub1.id

  connection {
    type        = "ssh"
    user        = "ubuntu"  # username for your EC2 instance
    private_key = file("~/Downloads/aws-login.pem")  # path to the private key
    host        = self.public_ip
  }

  # File provisioner to copy a file from local to the remote EC2 instance
  provisioner "file" {
    source      = "app.py"  # Replace with the path to your local file
    destination = "/home/ubuntu/app.py"  # Replace with the path on the remote instance
  }

  provisioner "remote-exec" {
    inline = [
      "echo 'Hello from the remote instance'",
      "sudo apt update -y",  # Update package lists (for ubuntu)
      "sudo apt-get install -y python3-pip",  # package installation
      "cd /home/thalla",
      "sudo pip3 install flask",
      "sudo python3 app.py",
    ]
  }
}

