#!/usr/bin/env python
# coding: utf-8

import urllib
import json

#bio_dict is the dictionary used to assign DBpedia URIs. When a specific key is
#found in the text, the value URI is returned. Any dictionary can be used here.

with open('biodict.txt', 'r') as file:
    bio_dict = eval(file.read())

in_file_name = "text_object_id1.txt"
out_file_name = "all_uri.txt"

#At this point, you have imported all the modules you need, read the dictionary
#you will use to the assign the URIs and opened all the files you will be using. The
#InFile should be a list of DataObject IDs. The OutFile will hold your results. Any blank
#lines in the input file will cause an error and the program will stop.

def get_data_object_url(line):
    return 'http://eol.org/api/data_objects/1.0/{}.json'.format(line)

#get_data_object_url is a function that will create the URL needed to query the API
#for each data object ID in the list

with open(in_file_name, 'r') as in_file, open(out_file_name, 'w') as out_file:
	for line in in_file:   
		line = line.strip()                                  
		results = urllib.urlopen(get_data_object_url(line)).read()
		data = json.loads(results)
		descriptions = data['dataObjects'][0]['description'].lower()  
		out_file_text = [','.join([line, key, bio_dict[key]]) for key in bio_dict if key in descriptions]
		out_file.write('\n'.join(out_file_text))

#This code goes over each line in the in_file (a list of text object IDs), retrieves
#them from the API in json format, pulls out the description text and then iterates over
#each key in the dictionary. If the key is found the value is returned and the system
#moves on to the next key. If the key is not found, the system returns nothing and moves
#on to the next key.