from sys import argv
import random
import re
import nltk
from nltk.corpus import cmudict
from nltk.probability import LidstoneProbDist

script, book = argv

e = cmudict.entries()
d = cmudict.dict()

print "importing source text..."
f = open(book)
print "reading source text..."
t = f.read()
print "tokenizing words..."
w = nltk.word_tokenize(t)


def make_word_list():
	print "making word list..."
	word_list = []
	for i in w:
		try:
			d[i.lower()]
		except KeyError:
			pass
		else:
			if i.lower() == "'s":
				pass
			elif i[-1] == ".":
				pass
			else:
				word_list.append((i.lower(), d[i.lower()][0]))
	return word_list
	
word_list = make_word_list()


def valid_words():
	print "extracting words from word list..."
	vw = []
	for (x, y) in word_list:
		vw.append(x)
	return vw
	
vw = valid_words()


def unique(s):
	print "making unique word list..."
	u = []
	for x in s:
		if x not in u:
			u.append(x)
		else:
			pass
	return u
    
word_list_u = unique(word_list)


def strip_numbers(x):
	xj = '.'.join(x)
	xl = re.split('0|1|2', xj)
	xjx = ''.join(xl)
	xlx = xjx.split('.')
	return xlx
	
	
def ends_in_vowel(pl):
	if 'A' in pl[-1:][0] or 'E' in pl[-1:][0] or \
	'I' in pl[-1:][0] or 'O' in pl[-1:][0] or \
	'U' in pl[-1:][0] or 'Y' in pl[-1:][0]:
		return True	
	else:
		return False


def contains_vowel(pl, n):
	if 'A' in pl[n][0] or 'E' in pl[n][0] or \
	'I' in pl[n][0] or 'O' in pl[n][0] or \
	'U' in pl[n][0] or 'Y' in pl[n][0]:
		return True	
	else:
		return False


def rhyme_finder(word):
	rhyming_words = []
	pron = strip_numbers(d[word][0])
	if len(pron) == 1:
		for (x, y) in word_list_u:
			ps = strip_numbers(y)
			if ps[-1] == pron[0]:
				rhyming_words.append(x)
			else:
				pass
	elif len(pron) == 2:
		if ends_in_vowel(pron):
			for (x, y) in word_list_u:
				ps = strip_numbers(y)
				if ps[-1] == pron[-1]:
					rhyming_words.append(x)
				else:
					pass
		else:
			for (x, y) in word_list_u:
				ps = strip_numbers(y)
				if ps[-2:] == pron:
					rhyming_words.append(x)
				else:
					pass
	elif len(pron) >= 3:
		if ends_in_vowel(pron):
			for (x, y) in word_list_u:
				ps = strip_numbers(y)
				if ps[-1] == pron[-1]:
					rhyming_words.append(x)
				else:
					pass
		else:
			if contains_vowel(pron, -2):
				for (x, y) in word_list_u:
					ps = strip_numbers(y)
					if ps[-2:] == pron[-2:]:
						rhyming_words.append(x)
					else:
						pass
			elif contains_vowel(pron, -3):
				for (x, y) in word_list_u:
					ps = strip_numbers(y)
					if ps[-3:] == pron[-3:]:
						rhyming_words.append(x)
					else:
						pass
			elif contains_vowel(pron, -4):
				for (x, y) in word_list_u:
					ps = strip_numbers(y)
					if ps[-4:] == pron[-4:]:
						rhyming_words.append(x)
					else:
						pass
			else:
				pass
	else:
		pass
	rw = [i for i in rhyming_words if not i == word]
	return rw
	

print "building content model..."
estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
content_model = nltk.NgramModel(3, w, estimator=estimator)


def generate():
	sw1 = random.randint(0, len(vw) - 2)
	sw2 = sw1 + 2
	starting_words = vw[sw1:sw2]
	line_1 = content_model.generate(10, starting_words)
	line_2 = content_model.generate(10, line_1[-2:])
	line_3 = content_model.generate(9, line_2[-2:])
	line_4 = content_model.generate(9, line_3[-2:])
	line_5 = content_model.generate(10, line_4[-2:])
	line_6 = content_model.generate(10, line_5[-2:])
	line_7 = content_model.generate(9, line_6[-2:])
	line_8 = content_model.generate(9, line_7[-2:])
	line_9 = content_model.generate(10, line_8[-2:])
	line_10 = content_model.generate(10, line_9[-2:])
	line_11 = content_model.generate(9, line_10[-2:])
	line_12 = content_model.generate(9, line_11[-2:])
	line_13 = content_model.generate(10, line_12[-2:])
	line_14 = content_model.generate(9, line_13[-2:])
	lines = [line_1, line_2, line_3, line_4, line_5, line_6,
			 line_7, line_8, line_9, line_10, line_11, line_12,
			 line_13, line_14]
	for i in lines:
		i.remove(i[-1])
		i.remove(i[-1])
	return lines
	
	
def write():
	sw1 = random.randint(0, len(w) - 50)
	sw2 = sw1 + 50
	starting_words = w[sw1:sw2]
	
	line_1 = content_model.generate(50, starting_words)
	line_1 = line_1[-50:]
	print ' '.join(line_1)
	line_1a = raw_input('> ')
	line_1a = nltk.word_tokenize(line_1a)
	
	line_2 = content_model.generate(50, line_1a)
	print ' '.join(line_2)
	line_2a = raw_input('> ')
	line_2a = nltk.word_tokenize(line_2a)
	
	line_3 = content_model.generate(50, line_2a)
	print ' '.join(line_3)
	print '_' * 10
	print ' '.join(rhyme_finder(line_1a[-1]))
	line_3a = raw_input('> ')
	line_3a = nltk.word_tokenize(line_3a)
	
	line_4 = content_model.generate(50, line_3a)
	print ' '.join(line_4)
	print '_' * 10
	print ' '.join(rhyme_finder(line_2a[-1]))
	line_4a = raw_input('> ')
	line_4a = nltk.word_tokenize(line_4a)
	
	line_5 = content_model.generate(50, line_4a)
	print ' '.join(line_5)
	line_5a = raw_input('> ')
	line_5a = nltk.word_tokenize(line_5a)
	
	line_6 = content_model.generate(50, line_5a)
	print ' '.join(line_6)
	line_6a = raw_input('> ')
	line_6a = nltk.word_tokenize(line_6a)
	
	line_7 = content_model.generate(50, line_6a)
	print ' '.join(line_7)
	print '_' * 10
	print ' '.join(rhyme_finder(line_5a[-1]))
	line_7a = raw_input('> ')
	line_7a = nltk.word_tokenize(line_7a)
	
	line_8 = content_model.generate(50, line_7a)
	print ' '.join(line_8)
	print '_' * 10
	print ' '.join(rhyme_finder(line_6a[-1]))
	line_8a = raw_input('> ')
	line_8a = nltk.word_tokenize(line_8a)
	
	line_9 = content_model.generate(50, line_8a)
	print ' '.join(line_9)
	line_9a = raw_input('> ')
	line_9a = nltk.word_tokenize(line_9a)
	
	line_10 = content_model.generate(50, line_9a)
	print ' '.join(line_10)
	line_10a = raw_input('> ')
	line_10a = nltk.word_tokenize(line_10a)
	
	line_11 = content_model.generate(50, line_10a)
	print ' '.join(line_11)
	print '_' * 10
	print ' '.join(rhyme_finder(line_9a[-1]))
	line_11a = raw_input('> ')
	line_11a = nltk.word_tokenize(line_11a)
	
	line_12 = content_model.generate(50, line_11a)
	print ' '.join(line_12)
	print '_' * 10
	print ' '.join(rhyme_finder(line_10a[-1]))
	line_12a = raw_input('> ')
	line_12a = nltk.word_tokenize(line_12a)
	
	line_13 = content_model.generate(50, line_12a)
	print ' '.join(line_13)
	line_13a = raw_input('> ')
	line_13a = nltk.word_tokenize(line_13a)
	
	line_14 = content_model.generate(50, line_13a)
	print ' '.join(line_14)
	print '_' * 10
	print ' '.join(rhyme_finder(line_13a[-1]))
	line_14a = raw_input('> ')
	line_14a = nltk.word_tokenize(line_14a)
	
	return [line_1a, line_2a, line_3a, line_4a, line_5a, line_6a, line_7a, line_8a,
			line_9a, line_10a, line_11a, line_12a, line_13a, line_14a]


def sylcount(s):
	try:
		sj = ''.join(d[s][0])
		sl = re.split('0|1|2', sj)
	except KeyError:
		return None
	else:
		return len(sl) - 1
		
		
def line_sylcount(line):
	count = 0
	for word in line:
		count += sylcount(word)
	return count


def couplet(x, y, lines):
	line_1 = lines[x]
	line_2 = lines[y]
	end_word_1 = line_1.pop()
	while end_word_1 in banned_end_words:
		end_word_1 = random.choice(vw)
	rhyming_words = rhyme_finder(end_word_1)
	while rhyming_words == []:
		end_word_1 = random.choice(vw)
		while end_word_1 in banned_end_words:
			end_word_1 = random.choice(vw)
		rhyming_words = rhyme_finder(end_word_1)
	end_word_2 = random.choice(rhyming_words)
	for _ in range(9):
		if line_sylcount(line_1) + sylcount(end_word_1) == 10:
			break
		else:
			over = line_sylcount(line_1) + sylcount(end_word_1) - 10
			for i in line_1:
				if sylcount(i) <= over:
					line_1.remove(i)
					break
				else:
					pass
	for _ in range(9):
		if line_sylcount(line_2) + sylcount(end_word_2) == 10:
			break
		else:
			over = line_sylcount(line_2) + sylcount(end_word_2) - 10
			for i in line_2:
				if sylcount(i) <= over:
					line_2.remove(i)
					break
				else:
					pass
	line_1.append(end_word_1)
	line_2.append(end_word_2)
	return [line_1, line_2]

	
def couplet_checker():
	lines = generate()
	c1 = couplet(0, 2, lines)
	c2 = couplet(1, 3, lines)
	c3 = couplet(4, 6, lines)
	c4 = couplet(5, 7, lines)
	c5 = couplet(8, 10, lines)
	c6 = couplet(9, 11, lines)
	c7 = couplet(12, 13, lines)
	while line_sylcount(c1[0]) != 10 or line_sylcount(c1[1]) != 10 or \
		  line_sylcount(c2[0]) != 10 or line_sylcount(c2[1]) != 10 or \
		  line_sylcount(c3[0]) != 10 or line_sylcount(c3[1]) != 10 or \
		  line_sylcount(c4[0]) != 10 or line_sylcount(c4[1]) != 10 or \
		  line_sylcount(c5[0]) != 10 or line_sylcount(c5[1]) != 10 or \
		  line_sylcount(c6[0]) != 10 or line_sylcount(c6[1]) != 10 or \
		  line_sylcount(c7[0]) != 10 or line_sylcount(c7[1]) != 10:
		lines = generate()
		c1 = couplet(0, 2, lines)
		c2 = couplet(1, 3, lines)
		c3 = couplet(4, 6, lines)
		c4 = couplet(5, 7, lines)
		c5 = couplet(8, 10, lines)
		c6 = couplet(9, 11, lines)
		c7 = couplet(12, 13, lines)
	return [c1[0], c2[0], c1[1], c2[1], c3[0], c4[0], c3[1], c4[1],
			c5[0], c6[0], c5[1], c6[1], c7[0], c7[1]]


def sonnetizer():
	s = write()
	l1 = ' '.join(s[0])
	l2 = ' '.join(s[1])
	l3 = ' '.join(s[2])
	l4 = ' '.join(s[3])
	l5 = ' '.join(s[4])
	l6 = ' '.join(s[5])
	l7 = ' '.join(s[6])
	l8 = ' '.join(s[7])
	l9 = ' '.join(s[8])
	l10 = ' '.join(s[9])
	l11 = ' '.join(s[10])
	l12 = ' '.join(s[11])
	l13 = ' '.join(s[12])
	l14 = ' '.join(s[13])
	sonnet = [l1, l2, l3, l4, l5, l6, l7, l8, 
			  l9, l10, l11, l12, l13, l14]
	return '\n' + '\n'.join(sonnet) + '\n'

sonnet = sonnetizer()
print sonnet
	
		