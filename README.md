pseudonitzchia
==============

Biodiversity informatics code relevant to the Encyclopedia of Life

names_json_1.py
Version 1 of a program that uses the EOL and GNRD APIs to generate a list of species that
interact with each other. The theory behind this idea is that if a species is mentioned 
in a text data object under the associations chapter of a taxon page, the mentioned 
species can be assumed to have an interaction with the topic taxon. This version of the 
program does not work on every taxon.

names_json_2.py
Version 2 is the same as Version 1, but it is cleaner (had some superfluous stuff 
deleted) and works across all taxa.

eco_terms_all_json.py
Version 1 of a program that annotates EOL text objects with DBpedia URIs.

replace_dict.txt
Version 1 of a dictionary that is used by the names_json program. 

biodict.txt
Version 1 of a dictionary that is used by the eco_terms_all_json program.

associations_all_revised.txt
The results from names_json_2.py only processing species level taxon pages. The numbers 
represent EOL taxon IDs. The first column is the EOL taxon ID for the taxon page that was 
mined. The second column is the EOL taxon ID for the taxon that was found in a text object 
on the taxon page for the taxon in the first column. There is an implied interaction 
between the two taxa in each row. The type of interaction is unknown.

Ready for discovery through http://globalbioticinteractions.org .
