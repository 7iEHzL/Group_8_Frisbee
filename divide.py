def divide(a,b):
	
	if (b!=0):
		return a/b
	else:
		print("Error: cannot divide by zero")
		quit()

x = int(input("x >"))
y = int(input("y >")) 
print("%d / %d = %.3f" % (x,y,divide(x,y)))
