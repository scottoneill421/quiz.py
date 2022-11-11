#!/usr/bin/python3

import sys, random, os, curses
from curses import wrapper
from curses.textpad import rectangle

flashCard = {
	"title":	"",
	"topic":	"",
	"question":	"",
	"answer":	[],
	"is_revealed":	False,
}

flashCardprev = {
	"title":	"",
	"topic":	"",
	"question":	"",
	"answer":	[],
	"is_revealed":	False,
}

def usage():
	"""Prints usage instructions"""
	print("Please enter a file to parse")
	print("Example: ./quiz.py file")
	print("Exiting...")

def getTopics(f):
	"""Grab each topic outlined in the file"""
	
	# Get contents of file, remove the excess newline characters
	content = f.readlines()
	content = list(filter(lambda x: x != '\n', content))

	# Grab title
	line = content.pop(0)
	line = content.pop(0)
	title = ""
	for i in line:
		if i not in ('='):
			title += i
	line = content.pop(0)

	# format content into a list of topics and their notes
	buffer  = []
	topics = {}
	topic = ""
	for line in content:
		if line[0] == '\t':
			buffer.append(line)
		else:
			if len(buffer) != 0:
				topics[topic] = buffer
				buffer = []
				topic = line
			topic = line
	topics[topic] = buffer
	return title, topics


def getQuestions(f):
	"""Takes Topics dict and returns a series of flashcards"""
	title, topics = getTopics(f)
	flashCards = []
	flashCard["title"] = title
	for topic in topics.keys():
		flashCard["topic"] = topic
		for line in topics[topic]:
			if line[1] != '\t':
				if len(flashCard["answer"]) > 0:
					flashCards.append(flashCard.copy())
					flashCard["answer"] = []
				flashCard["question"] = line
			else:
				flashCard["answer"].append(line)
		flashCards.append(flashCard.copy())
		flashCard["answer"] = []
	return flashCards

def setColours():
	"""Set apps colours"""
	curses.init_color(curses.COLOR_BLACK, 0, 0, 0)	
	curses.init_color(curses.COLOR_RED, 1000, 0, 0)
	curses.init_color(curses.COLOR_GREEN, 0, 1000, 0)
	curses.init_color(curses.COLOR_YELLOW, 1000, 1000, 0)
	curses.init_color(curses.COLOR_BLUE, 0, 0, 1000)
	curses.init_color(curses.COLOR_MAGENTA, 700, 0, 500)
	curses.init_color(curses.COLOR_CYAN, 0, 500, 700)
	curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)


def createWindows(w):
	"""define apps windows"""
	setColours()
	rtitle	  = rectangle(w, 1,  1,  3,  50)
	rtopic	  = rectangle(w, 4,  1,  6,  50)
	rquestion = rectangle(w, 7,  1,  10, 100)
	ranswer   = rectangle(w, 11, 1,  27, 100)  
	rinstr	  = rectangle(w, 1,  51, 6,  100)

	wtitle	  = curses.newwin(1,  45, 2,  2)
	wtopic	  = curses.newwin(1,  45, 5,  2)	
	wquestion = curses.newwin(2,  95, 8,  2)	
	wanswer   = curses.newwin(10, 95, 12, 2)	
	winstr	  = curses.newwin(4,  40, 2, 52)
	werror	  = curses.newwin(1,  45, 26,  3)

	w.refresh()

	windows = {
		"title":     	wtitle,
		"topic":    	wtopic,
		"question":  	wquestion,
		"answer":    	wanswer,
		"instr":     	winstr,
		"error":	werror,
	}
	return windows


def printText(windows, flashCard):
	"""print text on windows"""
	for w in windows.keys():
		windows[w].clear()

	windows["title"].addstr(flashCard["title"].strip())
	windows["topic"].addstr(flashCard["topic"].strip())
	windows["question"].addstr(flashCard["question"].strip())	
	windows["instr"].addstr("Q\tQuit Quiz\nSPACE\tReveal Answer\n")
	
	for w in windows.keys():
		windows[w].refresh()


def printAnswer(windows, flashCard):
	"""reveal answer of flashcard"""
	ans = ""
	for line in flashCard["answer"]:
		ans += line.strip('\t')
	windows["answer"].addstr(ans)

	flashCard["is_revealed"] = True
	windows["answer"].refresh()

def printError(windows, c):
	"""Displays error if incorrect key pressed"""
	windows["error"].clear()
	errorText = "{0} is not a valid key".format(chr(c))
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	windows["error"].addstr(errorText.strip(), curses.color_pair(1))
	windows["error"].refresh()


def keyHandler(windows, flashCard):
	"""handles user selection"""
	c = windows["answer"].getch()
	if c == ord('q'):
		exit()
	elif c == ord(' '):
		if flashCard["is_revealed"]:
			flashCard["is_revealed"] = False
			return
		else:
			printAnswer(windows, flashCard)
			keyHandler(windows, flashCard)	
	else:
		printError(windows, c)
		keyHandler(windows, flashCard)


def main(w):
	notes = sys.argv[1:]


	flashCards = []
	
	for i in notes:
		with open(i, 'r') as f:
			flashCards += getQuestions(f)
			

	windows = createWindows(w)
	flashCard = {}
	while True:
		flashCard = flashCards[random.randrange(0, len(flashCards))]
		printText(windows, flashCard)
		keyHandler(windows, flashCard)


if len(sys.argv[1:]) < 1:
	usage()
	exit()
else:
	wrapper(main)
