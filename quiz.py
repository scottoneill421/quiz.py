#!/usr/bin/python3
import os, sys
import getopt
import re
import random

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

	return cards


def present_card(cards):
	"""Presents a question, prompt user, then provide answer"""
	os.system('clear')
	
	length = len(cards)
	keys = list(cards.keys())
	
	i = random.randint(0, length - 1)
	k = keys[i]
	
	ul = ""
	i = 0
	while i < len(k):
		ul += '-'
		i += 1

	print(k)
	kp = input(ul)
	kp = input(cards[k])


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
		cards = get_cards(notes)
		present_card(cards)
	else:
		usage()

if __name__ == "__main__":
	main(sys.argv[1:])
