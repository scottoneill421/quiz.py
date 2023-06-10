#!/usr/bin/python3
import sys
import getopt

def get_notes(file):
	with open(file, "r") as f:
		notes = f.readlines()
	
	notes = [line.strip() for line in notes]

	return notes

def usage():
	print("Usage: quiz.py -r <file> or quiz.py --read <file>")

def main(argv):
	file = None

	try:
		opts, args = getopt.getopt(argv, "hr:", ["help", "read="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-r", "--read"):
			file = arg
	
	if file is not None:
		notes = get_notes(file)
	
		for note in notes:
			print(note)

	else:
		usage()

if __name__ == "__main__":
	main(sys.argv[1:])
