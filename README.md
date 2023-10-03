# Zero Touch Deployment - Terraform

## Project Overview

The Zero Touch Deployment project focuses on automating the deployment of an auction application for cricket, designed for the University of Hyderabad's HCU Premier League 5. This application allows users to view participating teams' information, player statistics, and conduct auctions. It's built using Python Flask and deployed on AWS infrastructure provisioned using Terraform.

## Features

- Home page with participating team information.
- Random player stats display with options for sold and unsold players.
- Auction functionality to add players to teams or mark them as unsold.
- Automatic generation of team player lists with images, stats, contact details, and bid prices.

## Prerequisites

Before deploying this application, ensure you have the following prerequisites:

1. AWS account with credentials configured.
2. Terraform installed on your local machine.
3. Python and Flask installed.

## Deployment Steps

1. **Clone the Repository**: Clone this repository to your local machine:

    ```shell
    git clone https://github.com/yourusername/zerotouch-deployment.git
    cd zerotouch-deployment
    ```

2. **AWS Configuration**: Configure your AWS credentials and region. Replace `<your-aws-access-key>` and `<your-aws-secret-key>` with your AWS IAM user's credentials in the `~/.aws/credentials` file.

    ```shell
    [default]
    aws_access_key_id = <your-aws-access-key>
    aws_secret_access_key = <your-aws-secret-key>
    region = us-east-1  # Replace with your desired region
    ```

3. **Terraform Deployment**: Use Terraform to provision the AWS infrastructure:

    ```shell
    cd terraform
    terraform init
    terraform plan
    terraform apply
    ```

4. **Application Deployment (Local)**: Install Flask and run the application:

    ```shell
    cd ..
    pip install flask
    python app.py
    ```

5. **Access the Application**: Open a web browser and go to `http://<your-ec2-instance-public-ip>:5000` to access the auction application.

## Usage

1. Browse the application to view participating teams and player statistics.
2. Conduct auctions by clicking on the "Add to Team" or "Mark as Unsold" buttons.
3. Completed auctions will generate team player lists with comprehensive details.

## Cleanup

To destroy the AWS resources and terminate the application:

```shell
cd terraform
terraform destroy
