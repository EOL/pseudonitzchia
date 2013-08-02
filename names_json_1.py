#!/usr/bin/env python
# coding: utf-8
from __future__ import division
import urllib2, urllib, time
from bs4 import BeautifulSoup
import json
DEBUG = 1

def dbg(var):
	if DEBUG: print var
#This function prints the results of several actions. The "DEBUG" above should be 0 to
#turn all off or 1 to turn all on
	
def data_object_url(line):
	return 'http://eol.org/api/pages/1.0/' + line.strip() + '.json?images=0&videos=0&sounds=0&maps=0&text=75&iucn=false&subjects=associations&licenses=all&details=true&com'
#This function calls the EOL API to get all text data objects under a specific chapter. 
#In URL above, subjects=<can have 'associations', 'trophicstrategy', 'habitat', 'ecology', etc>

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
#This function calls a dictionary to find and replace characters in the html that interfere
#with GNRD ability to find names

def id_to_texts(eol_id, replace_dict):
	"""
	Given an EOL Taxon ID, return the text data objects as a list
	
	Returns empty list if the server does not give a proper response.
	"""
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
	print texts
	return texts
		
def texts_to_tokens(texts):
	"""
	Given a list of text data objects, submit each to the GNRD API and 
	return a list of token urls that have the results.
	"""
	return [text_to_token(text) for text in texts]
		
def text_to_token(texts):
	"""
	Given a single text data object, submit it to the GNRD API and get a token url
	which we can query for the species results
	"""
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
	
def check_tokens(gnrd_token_url):
	"""
	Given a list of gnrd token urls, submit each to the GNRD API to get back the actual
	results.
	"""
	return [check_token(token_url) for token_url in gnrd_token_url]
	
def check_token(gnrd_token_url):
	"""
	Given a single token url, check with GNRD to get the results
	"""
	#ready = None
	#while ready == None:
	#print gnrd_token_url [0]
	#gnrd_results = []
	print 'gnrd_token_url = ' + str(gnrd_token_url)
	for token_url in gnrd_token_url:
		time.sleep(5)
		names = urllib2.urlopen(token_url)
		#ready = []
		name_results = names.read()
		names.close()
		gnrd_results.append(name_results)
	dbg('gnrd_results =' + str(gnrd_results) + '\n')
	return gnrd_results
	
def get_names_list(gnrd_results):
	"""
	Given the GNRD results, grab the actual names
	"""
	#name_list = []
	print len(gnrd_results)
	for result in gnrd_results:
		gnrd_names = json.loads(result)
		names_list = gnrd_names.get('names', None)
		print type(names_list)
		print len(names_list)
		dbg('name list =' + str(names_list) + '\n')
		for taxon in names_list:
			taxon_name = taxon.get('identifiedName',None)
			print taxon_name
			name_list.append(taxon_name)
	return name_list

def get_resolver_results(gnrd_results):
	"""
	Given the GNRD results, grab the resolver results
	"""
	eol_resolved = []
	for name in gnrd_results:
		load_names = json.loads(name)
		resolved_names = load_names.get('resolved_names', None)
		eol_resolved.append(resolved_names)
	dbg('eol_resolved =' +str(eol_resolved) + '\n')
	print type(eol_resolved)
	print len(eol_resolved)
	return eol_resolved
	
def get_topic_id(eol_resolved):
	"""
	Given the resolver results, grab the actual topic taxon IDs
	"""
	for resolved in eol_resolved:
		if resolved != None:
			dbg('results =' + str(resolved) + '\nresults data type =' + str(type(resolved)) + str(len(resolved)))
			if len(resolved) > 1:
				#results1 = results[1]
				#dbg('results1 =' + str(results1) + '\nresults1 data type =' + str(type(results1)))
				for results in resolved:
					load_results = json.loads(results)
					results1 = load_results.get('results', None)
					dbg('results1 =' + str(results1) + '\nresults1 data type =' + str(type(results1)))
					results2 = results1[0]
					dbg('results2 =' + str(results2) + '\nresults2 data type =' + str(type(results2)))
					eol_url = results2 ['url']
					dbg('eol_url =' + str(eol_url) + '\neol_url data type =' + str(type(eol_url)))
					eol_url_list.append(eol_url)
	print eol_url_list
	print type(eol_url_list)	
	return eol_url_list
					#output(
	
def output(eol_url_list):
	"""
	Send results to an outfile
	"""
	print name_list
	if name_list != None:
		for url in eol_url_list:
			out_file.write(line.strip() + ',' + str(url).replace('http://eol.org/pages/','') + '\n')		

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
	#gnrd_name = get_names_gnrd_names(gnrd_results)
	output(get_topic_id(get_resolver_results(gnrd_results)))