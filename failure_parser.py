def parseList():
	with open("FailureMode.txt", "r") as f:
		text = f.read()

	text = text.strip()

	x = text.split("\n")

	return x