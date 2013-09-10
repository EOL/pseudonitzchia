#!/usr/bin/env python
# coding: utf-8
from __future__ import division
import urllib2, urllib, time
from bs4 import BeautifulSoup
import json
DEBUG = 0

"""
This code uses two APIs and several functions to build a list of species interactions. 
The input is a list of EOL species IDs. The output is a two column list of the EOL ID for 
the look-up taxa (from the list of EOL IDs; first column) and the EOL ID of the taxon 
that has a relationship with the look-up taxon (second column). 
"""

def dbg(var):
	if DEBUG: print var
"""
This function prints the results of several actions. The "DEBUG" above should be 0 to
turn all off or 1 to turn all on
"""
	
def data_object_url(line):
	return 'http://eol.org/api/pages/1.0/' + line.strip() + '.json?images=0&videos=0&sounds=0&maps=0&text=75&iucn=false&subjects=associations|trophicstrategy|habitat|ecology&licenses=all&details=true&com'
"""
This function generates the URL to call the EOL API to get all text data objects for a taxon under a specific 
chapter in json format. In URL above, text is retrieved from under the 'associations', 
'trophicstrategy', 'habitat', 'ecology' chapter.
"""

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
"""
This function calls a dictionary to find and replace characters in html that 
interfere with GNRD ability to find names
"""

def id_to_texts(eol_id, replace_dict):
	texts = []
	results = urllib.urlopen(data_object_url(eol_id)).read()
	if results [3:8] == 'error':
		return []
	data = json.loads(results)
	for info in data['dataObjects']:
		dbg('text = ' + str(info) + '\n')
		text = info['description']
		soup = BeautifulSoup(replace_all(text, replace_dict))
		clean = soup.get_text()
		texts.append(clean)
	return texts
"""
Given an EOL Taxon ID, this function returns the text data objects (from the json API 
output) as a list. Returns empty list if the server does not give a proper response. 
Beautiful Soup is used to clean the html tags from the text.
"""
		
def text_to_token(texts):
	for text in texts:
		dbg('clean text =' + text + '\n')
		url_clean = urllib2.quote(text.encode('ascii','replace'))
		gnrd = 'http://gnrd.globalnames.org/name_finder.json'
		gnrd_content = urllib2.urlopen(gnrd, 'text=' + url_clean + '&data_source_ids=12')
		gnrd_results = gnrd_content.read()
		gnrd_content.close()
		dbg('gnrd json =' + gnrd_results + '\n')
		gnrd_data = json.loads(gnrd_results)
		token_url = gnrd_data.get('token_url', None)
		dbg('token url =' + repr(token_url) + '\n')
		gnrd_token_url.append(token_url)
	return gnrd_token_url
"""
Given a single text data object, submit it to the GNRD API and get a token url
which we can query for the species results
"""
	
def check_token(gnrd_token_url):
	dbg('gnrd_token_url = ' + str(gnrd_token_url) + '\n')
	for token_url in gnrd_token_url:
		time.sleep(5)
		names = urllib2.urlopen(token_url)
		name_results = names.read()
		names.close()
		gnrd_results.append(name_results)
	dbg('gnrd_results =' + str(gnrd_results) + '\n')
	return gnrd_results
"""
Given a single token url, check with GNRD to get the results
"""
	
def get_names_list(gnrd_results):
	for result in gnrd_results:
		gnrd_names = json.loads(result)
		names_list = gnrd_names.get('names', None)
		dbg('name list =' + str(names_list) + '\n')
		for taxon in names_list:
			taxon_name = taxon.get('identifiedName',None)
			name_list.append(taxon_name)
	return name_list
"""
Given the GNRD results, grab the actual names
"""

def get_resolver_results(gnrd_results):
	eol_resolved = []
	for name in gnrd_results:
		load_names = json.loads(name)
		resolved_names = load_names.get('resolved_names', None)
		eol_resolved.append(resolved_names)
	dbg('eol_resolved =' +str(eol_resolved) + '\n')
	return eol_resolved
"""
Given the GNRD results, grab the resolver results
"""
	
def get_topic_id(eol_resolved):
	for resolved in eol_resolved:
		if resolved != None:
			dbg('resolved =' + str(resolved) + '\nresolved data type =' + str(type(resolved)) + str(len(resolved)))
			if len(resolved) > 1:
				for results in resolved:
					results1 = results.get('results', None)
					dbg('results1 =' + str(results1) + '\nresults1 data type =' + str(type(results1)))
					if results1 != None:
						results2 = results1[0]
						dbg('results2 =' + str(results2) + '\nresults2 data type =' + str(type(results2)))
						eol_url = results2 ['url']
						dbg('eol_url =' + str(eol_url) + '\neol_url data type =' + str(type(eol_url)))
						eol_url_list.append(eol_url)
	return eol_url_list
"""
Given the resolver results, grab the actual topic taxon IDs
"""
	
def output(eol_url_list):
	if name_list != None:
		for url in eol_url_list:
			out_file.write(line.strip() + ',' + str(url).replace('http://eol.org/pages/','') + '\n')
"""
Send results to an outfile
"""		

def main():
	in_file_name = "species_id.txt"
	in_file = open(in_file_name, 'r')
	out_file_name = "all_name.txt"
	out_file = open(out_file_name, 'w')
	replace_dict = eval(open('replace_dict.txt').read())
	

if __name__ == "__main__":
	main()

in_file_name = "species_id1.txt"
in_file = open(in_file_name, 'r')
out_file_name = "all_name.txt"
out_file = open(out_file_name, 'w')
replace_dict = eval(open('replace_dict.txt').read())
	
main()
for line in in_file:
	print line
	gnrd_token_url = []
	gnrd_results = []
	name_list = []
	gnrd_name = []
	eol_url_list = []
	gnrd_results = check_token(text_to_token(id_to_texts(line, replace_dict)))
	name_list = get_names_list(gnrd_results)
	output(get_topic_id(get_resolver_results(gnrd_results)))