#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

with open('tass_page_data.json', 'r') as fp:
	list_input = json.load(fp)

with open('pnp_page_data.json', 'r') as fp:
	list_input0 = json.load(fp)

list_input = list_input + list_input0


for x in list_input:

	string_text = dehtml(x['text']);
	string_text = string_text.replace('\n', ' ')
	string_text = string_text.lower().encode('utf8')

        # TODO replace this section with a regex.
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
	for y in x['list_words']:
		print y


def function_count_words(list_tup_words_count,x):
	for y in x['list_words']:
		flag = False
		for i, v in enumerate(list_tup_words_count):
			if y == v[0]:
				list_tup_words_count[i] = (list_tup_words_count[i][0],list_tup_words_count[i][1] + 1) 
				flag = True
				break;
		if flag == False:
			list_tup_words_count.append((y,1))
	return list_tup_words_count

def load_words_count_file(string_filename):
	list_tup_words_count = []

	with open(string_filename, 'r') as f:
		old_file_position = f.tell()
		f.seek(0, os.SEEK_END)
		size = f.tell()
		f.seek(old_file_position, os.SEEK_SET)
		if(size>0):
			list_tup_words_count = json.loads(f.read())

			for i, v in enumerate(list_tup_words_count):
				list_tup_words_count[i] = (list_tup_words_count[i][0].encode('utf-8'),list_tup_words_count[i][1]) 
	return list_tup_words_count

def write_file_words_count(list_tup_words_count, list_tup_words_count_name):
	list_words_count = sorted(list_tup_words_count, key=itemgetter(1), reverse=True)
	del list_words_count[500:] #Max 500 words.

	with open(list_tup_words_count_name, 'w') as f:
		f.write(json.dumps(list_words_count))
	return 0

list_tup_words_count_politics = load_words_count_file('list_tup_words_count_politics')
list_tup_words_count_army = load_words_count_file('list_tup_words_count_army')
list_tup_words_count_nature = load_words_count_file('list_tup_words_count_nature')
list_tup_words_count_economics = load_words_count_file('list_tup_words_count_economics')
list_tup_words_count_society = load_words_count_file('list_tup_words_count_society')
list_tup_words_count_world = load_words_count_file('list_tup_words_count_world')
list_tup_words_count_sensationalism = load_words_count_file('list_tup_words_count_sensationalism')
list_tup_words_count_culture = load_words_count_file('list_tup_words_count_culture')
list_tup_words_count_legal = load_words_count_file('list_tup_words_count_legal')
list_tup_words_count_local = load_words_count_file('list_tup_words_count_local')

# TODO a moving average.

for x in list_input:
	if(x['section']=='politics' or x['section']=='politika'):
		x['section']='политика'
		list_tup_words_count_politics = function_count_words(list_tup_words_count_politics,x)

	elif(x['section']=='army' or x['section']=='armiya-i-opk'):
		x['section']='армия'
		list_tup_words_count_army = function_count_words(list_tup_words_count_army,x)

	elif(x['section']=='science' or x['section']=='nauka' or x['section']=='kosmos'):
		x['section']='наука'
		list_tup_words_count_nature = function_count_words(list_tup_words_count_nature,x)

	elif(x['section']=='economics' or x['section']=='ekonomika' or x['section']=='msp' or x['section']=='nedvizhimost'):
		x['section']='экономика'
		list_tup_words_count_economics = function_count_words(list_tup_words_count_economics,x)

	elif(x['section']=='social' or x['section']=='obschestvo'):
		x['section']='общество'
		list_tup_words_count_society = function_count_words(list_tup_words_count_society,x)

	elif(x['section']=='world' or x['section']=='mezhdunarodnaya-panorama'):
		x['section']='мирские_дела'
		list_tup_words_count_world = function_count_words(list_tup_words_count_world,x)

	elif(x['section']=='incident' or x['section']=='proisshestviya'):
		x['section']='сенсационные_новости'
		list_tup_words_count_sensationalism = function_count_words(list_tup_words_count_sensationalism,x)

	elif(x['section']=='culture' or x['section']=='kultura'):
		x['section']='культура'
		list_tup_words_count_culture = function_count_words(list_tup_words_count_culture,x)

	elif(x['section']=='state-duma' or x['section']=='federation-council'):
		x['section']='законный'
		list_tup_words_count_legal = function_count_words(list_tup_words_count_legal,x)

	elif(x['section']=='regions' or x['section']=='moskva' or x['section']=='moskovskaya-oblast' or x['section']=='spb-news' or x['section']=='ural-news' or x['section']=='sibir-news'):
		x['section']='местный'
		list_tup_words_count_local = function_count_words(list_tup_words_count_local,x)


write_file_words_count(list_tup_words_count_politics,'list_tup_words_count_politics')
write_file_words_count(list_tup_words_count_army,'list_tup_words_count_army')
write_file_words_count(list_tup_words_count_nature,'list_tup_words_count_nature')
write_file_words_count(list_tup_words_count_economics,'list_tup_words_count_economics')
write_file_words_count(list_tup_words_count_society,'list_tup_words_count_society')
write_file_words_count(list_tup_words_count_world,'list_tup_words_count_world')
write_file_words_count(list_tup_words_count_sensationalism,'list_tup_words_count_sensationalism')
write_file_words_count(list_tup_words_count_culture,'list_tup_words_count_culture')
write_file_words_count(list_tup_words_count_legal,'list_tup_words_count_legal')
write_file_words_count(list_tup_words_count_local,'list_tup_words_count_local')

