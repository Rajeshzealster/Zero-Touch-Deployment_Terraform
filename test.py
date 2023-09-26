f=open('player_details.csv', 'r')
g=open('player.csv', 'a')
for i in f:
	l=i.split(",")
	l[2]="../"+l[2]
	g.write(",".join(l))
f.close()
g.close()
