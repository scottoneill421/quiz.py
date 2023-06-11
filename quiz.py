#!/usr/bin/python3
import os, sys
import getopt
import re
import random

from getch import getch

def usage():
	print("Usage: quiz.py -r <file> or quiz.py --read <file>")


def get_notes(file):
	"""open file, return lines as list"""
	with open(file, "r") as f:
		notes = f.readlines()
	
	notes = [line for line in notes]

	return notes


def get_cards(notes):
	"""take list from get_notes, turn into a dict"""
	cards = {}
	key = None
	val = ""

	for i in notes:
		#remove all leading whitespace except \t
		i = re.sub(r"^(?![\t])[ \t]+", "", i)

		#skip comments, make key value pairs, 
		#not tabbed = key, proceeding tabbed lines = values
		if i and not i.startswith('#'):
			if not i.startswith("\t"):
				if key is not None:
					cards[key] = val
					val = ""
				key = i.strip()
			else:
				val += i[1:] if i.startswith("\t") else i

	
	if key is not None:
		cards[key] = val.strip()

	# clear weird empty key/value pair
	if '' in cards and cards[''] == '':
		del cards['']

	return cards


def run_quiz(file):
	"""Presents a question, prompt user, then provide answer"""
	if file is None:
		usage()
		sys.exit(2)
	else:
		notes = get_notes(file)
		cards = get_cards(notes)
	
	kp = ""
	while True:
		os.system('clear')

		#define key variables
		length = len(cards)
		keys = list(cards.keys())	
		i = random.randint(0, length - 1)
		k = keys[i]
		ul = ""
		i = 0
		
		#create border string
		while i < len(k):
			ul += '-'
			i += 1

		#print out the question
		print(k + '\n' + ul + '\n\n' + ul)
		print("any:\treveal answer\nq:\tquit\n")
		c = getch()
		if c.lower() == 'q':
			print("Quitting...")
			sys.exit()
		os.system('clear')
		
		#print out the question with answer
		print(k + '\n' + ul + '\n')
		print(cards[k].rstrip() + '\n\n' + ul)
		print("any:\treveal answer\nq:\tquit\n")
		c = getch()
		if c.lower() == 'q':
			print("Quitting...")
			sys.exit()
			


def main(argv):
	file = None

	# confirm user input is valid, if not valid getopt, ERR
	try:
		opts, args = getopt.getopt(argv, "hr:", ["help", "read="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	# define user options, read/help
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-r", "--read"):
			run_quiz(arg)

	
	# run program

if __name__ == "__main__":
	main(sys.argv[1:])
