#!/usr/bin/python3
import os, sys
import getopt
import re
import random

from getch import getch

def usage():
	print("Usage: quiz.py -r <file> or quiz.py --read <file>")


def get_notes(files):
	"""open file, return lines as list"""
	# If only one string, convert to a list
	if isinstance(files, str):
		files = [files]

	notes = []
	for file in files:
		with open(file, "r") as f:
			buffer = []
			buffer.append(file)
			buffer.extend(f.readlines())
			notes.append(buffer)
	return notes


def get_cards(notes):
	"""take list from get_notes, turn into a dict"""
	cards = {}
	
	for entry in notes:
		chapter = entry[0]
		cards[chapter] = {}
		key = None
		val = ''

		for line in entry[1:]:
			if line.strip() and not line.startswith('#'):
				if not line.startswith('\t'):
					if key is not None:
						cards[chapter][key] = val.strip()
					key = line
					val = ''
				else:
					val += line
		
		if key is not None and val:
			cards[chapter][key] = val.strip()
	return cards

def gen_templates(file):
	"""generates template notes files based on contents"""
	if file is None:
		usage()
		sys.exit(2)
	
	templates = {}
	key = None
	val = []

	notes = get_notes(file)
	# generate a dictionary of chapters and their relevant topics.
	for i in notes[0][1:]:
		i = i.strip()
		if i and i[0].isdigit():
			if key is not None and val:
				templates[key.lower()] = val
				val = []
			key = i.replace('.', '').replace(' ', '-')
		elif i and i[0] == '-':
			val.append(i.replace('-', '').strip())

	# add last item after loop completes
	if key is not None and val:
		templates[key.lower()] = val

	# take the dictionary and make template notes files
	for key, value in templates.items():
		file = key + ".notes"
		with open(file, 'w') as f:
			f.write('# ' + key[2:].replace('-', ' ').title() + "\n\n")
			for i in value:
				f.write(i + "\n\n")


def run_quiz(files):
	"""Presents a question, prompt user, then provide answer"""
	if files is None:
		usage()
		sys.exit(2)
	else:
		notes = get_notes(files)
		cards = get_cards(notes)
	
	chapters = cards.keys()

	for chapter in chapters:
		title = chapter.replace('-', ' ').replace('.notes', '').title()
		i = 0
		border = ""
		while i < len(chapter):
			border += '-'
			i += 1
		
		topics = cards[chapter].keys()
		for topic in topics:
			os.system('clear')
			print('\033[1m' + title + '\033[0m' + '\n\n' + topic.strip() + '\n' + border + '\n\n' + border)
			print("any:\treveal answer\nq:\tquit\n")
			c = getch()
			if c.lower() == 'q':
				print("Quitting...")
				sys.exit()
			
			os.system('clear')
			print('\033[1m' + title + '\033[0m' + '\n\n' + topic.strip() + '\n' + border + '\n')
			print(cards[chapter][topic].rstrip() + '\n\n' + border)
			print("any:\tnext question\nq:\tquit\n")
			c = getch()
			if c.lower() == 'q':
				print("Quitting...")
				sys.exit()


def main(argv):
	# confirm user input is valid, if not valid getopt, ERR
	try:
		opts, args = getopt.getopt(argv, "hrt:", ["help", "read=", "template="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	# define user options, read/help
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-r", "--read"):
			files = argv[1:]
			run_quiz(files)
		elif opt in ("-t", "--template"):
			file = argv[1]
			gen_templates(file)
			print("Note files generated.")

if __name__ == "__main__":
	main(sys.argv[1:])
