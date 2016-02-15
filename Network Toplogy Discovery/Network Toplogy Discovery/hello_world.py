state = True
while(state):
	print "What are you thinking ?"
	a = raw_input("Input : ")
	print "Output : " + str(a)
	if a == "exit":
		state = False