#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
decoder = json.JSONDecoder()
import subprocess
from ast import literal_eval
from operator import itemgetter, attrgetter, methodcaller

from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc


def load_words_count_file(string_filename, string_type):
	with open(string_filename) as f:
		list_list = [list(literal_eval(line)) for line in f]

	list_tup_words_count = []

	for x in list_list[0]:
		list_tup_words_count.append((x[0].decode('unicode_escape').encode('utf-8'),x[1]))

	int_total = 0

	for x in list_tup_words_count:
		int_total = int_total + x[1]

	return (string_type,list_tup_words_count,int_total)

list_tup_words = []
list_tup_words.append(load_words_count_file('list_tup_words_count_politics','политика'))
list_tup_words.append(load_words_count_file('list_tup_words_count_army','армия'))
list_tup_words.append(load_words_count_file('list_tup_words_count_nature','наука'))
list_tup_words.append(load_words_count_file('list_tup_words_count_economics','экономика'))
list_tup_words.append(load_words_count_file('list_tup_words_count_society','общество'))
list_tup_words.append(load_words_count_file('list_tup_words_count_world','мирские_дела'))
list_tup_words.append(load_words_count_file('list_tup_words_count_sensationalism','сенсационные_новости'))
list_tup_words.append(load_words_count_file('list_tup_words_count_culture','культура'))
list_tup_words.append(load_words_count_file('list_tup_words_count_legal','законный'))
list_tup_words.append(load_words_count_file('list_tup_words_count_local','местный'))

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


with open('stopwords_russian', 'r') as fp:
	list_stopwords = fp.readlines()

list_stopwords = [x.strip() for x in list_stopwords] 

with open('page_data.json', 'r') as fp:
	list_input = json.load(fp)

for x in list_input:

	string_text = dehtml(x['text']);
	string_text = string_text.replace('\n', ' ')
	string_text = string_text.lower().encode('utf8')

        # TODO: replace with a regex.
	#string_result_stemmed = '';
	string_text = string_text.replace('"', ' ')
	string_text = string_text.replace('.', ' ')
	string_text = string_text.replace(',', ' ')
	string_text = string_text.replace('-', ' ')
	string_text = string_text.replace('—', ' ')
	string_text = string_text.replace('_', ' ')
	string_text = string_text.replace('(', ' ')
	string_text = string_text.replace(')', ' ')
	string_text = string_text.replace('[', ' ')
	string_text = string_text.replace('{', ' ')
	string_text = string_text.replace('}', ' ')
	string_text = string_text.replace(':', ' ')
	string_text = string_text.replace(';', ' ')
	string_text = string_text.replace('«', ' ')
	string_text = string_text.replace('»', ' ')
	string_text = string_text.replace('\xc2\xa0', ' ') 
	string_text = string_text.replace(' ', '\n')

	with open('somefile', 'w') as the_file:
		the_file.write(string_text)

	output=subprocess.check_output( './stemwords -l ru -i somefile', shell=True)
	list_words = output.splitlines()
	int_range = len(list_words); 

	int_i = 0
	while (int_i<int_range):
		list_words[int_i] = list_words[int_i].strip()
		if not list_words[int_i]:
			del list_words[int_i]
			int_range = len(list_words); 
		else:
			if (list_words[int_i] in list_stopwords) or list_words[int_i].isalnum() or len(list_words[int_i])==1:
				del list_words[int_i]
				int_range = len(list_words); 
			else:
				int_i = int_i + 1
	x['list_words'] = list_words

for x in list_input:
	list_scores = []
	for i, y in enumerate(list_tup_words):
		list_scores.append(0)
	for i, y in enumerate(list_tup_words):
		for z0 in y[1]:
			for z1 in x['list_words']:
				if(z0[0]==z1): 
					list_scores[i] = list_scores[i] + z0[1]
	for i, y in enumerate(list_tup_words):
		if(y[2]>0): list_scores[i] = float(list_scores[i]) / float(y[2])
		else: list_scores[i] = 0

	int_index = list_scores.index(max(list_scores))
	x['section'] = list_tup_words[int_index][0]

with open('classified_news', 'w') as f:
	f.write(json.dumps(list_input))

