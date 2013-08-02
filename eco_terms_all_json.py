#!/usr/bin/env python
# coding: utf-8
from __future__ import division
import urllib, json

#bio_dict is the dictionary used to assign DBpedia URIs. When a specific key is
#found in the text, the value URI is returned. Any dictionary can be used here.

bio_dict = eval(open('biodict.txt').read())

in_file_name = "text_object_id1.txt"
in_file = open(in_file_name, 'r')
out_file_name = "all_uri.txt"
out_file = open(out_file_name, 'w')

#At this point, you have imported all the modules you need, read the dictionary
#you will use to the assign the URIs and opened all the files you will be using. The
#InFile should be a list of DataObject IDs. The OutFile will hold your results. 

def data_object_url(line):
    return 'http://eol.org/api/data_objects/1.0/' + line.strip() + '.json'

#data_object_url is a function that will create the URL needed to query the API
#for each data object ID in the list

for line in in_file:										
    results = urllib.urlopen(data_object_url(line)).read()
    print line
    print len(results)
    data = json.loads(results)
    descriptions = data ['dataObjects'][0]['description'].lower()   
    for k, v in bio_dict.iteritems(): 
		if k in descriptions:
			out_file.write(','.join([line.strip(),k,v + '\n']))																																										
in_file.close()																							
out_file.close()

#This code goes over each line in the in_file (a list of text object IDs), retrieves
#them from the API in json format, pulls out the description text and then iterates over
#each key in the dictionary. If the key is found the value is returned and the system
#moves on to the next key. If the key is not found, the system returns nothing and moves
#on to the next key. Line 35 controls the format of the output. Lines 29 and 30 serve to
#show progress as the program runs.
#in the terminal and the code runs.