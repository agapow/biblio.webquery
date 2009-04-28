#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various utilities.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import re


### CONSTANTS & DEFINES ###

# patterns for extracting author info
STRIP_PATS = [re.compile (x, flags=re.IGNORECASE+re.UNICODE) for x in
	[
		r'^((edited )?by\s+)',   # "(edited )by ..."
		r'\s*, editors\.?$',     # "..., editors"
		r'^editors,?\s*',        # "editors, ..."
		r'\s*;\s+with an introduction by .*$',
		r'^\[\s*',               
		r'\s*\]$',
		r'\.{3,}',               # "..."
		r'et[\. ]al\.',          # "et al."
		r'\[',
		r'\]',
		r'\([^\)]+\)',          
	]
]
AND_PAT = re.compile (r'\s+and\s+')


### IMPLEMENTATION ###

def parse_name (name_str):
	"""
	Clean up a name into a more consistent format.

	:Parameters:
		name_str : string
			The "author" attribute from a Xisbn record in XML.
	
	:Returns:
		A list of the authors in "reverse" format, e.g. "['Smith, A. B.',
		'Jones, X. Y.']"

	Xisbn data can be irregularly formatted, unpredictably including
	ancillary information. This function attempts to cleans up the author field
	into a list of consistent author names.
	
	For example::

		>>> parse_authors ("Leonard Richardson and Sam Ruby.")
		['Richardson, Leonard', 'Ruby, Sam']
		>>> parse_authors ("Ann Thomson.")
		['Thomson, Ann']
		>>> parse_authors ("Stephen P. Schoenberger, Bali Pulendran, editors.")
		['Schoenberger, Stephen P.', 'Pulendran, Bali']
		>>> parse_authors ("Madonna")
		['Madonna']

	"""
	# TODO: Xisbn authors fields are often appended with extra information
	# like "with a foreword by" etc. Largely these are separated from the
	# author list by semi-colons and so should be easy to strip off.
	
	## Preconditions & preparation:
	# clean up string and return trivial cases 
	name_str = name_str.strip()
	if (not name_str):
		return []
	# strip extraneous and replace 'and'
	for pat in STRIP_PATS:
		name_str = pat.sub ('', name_str)
	name_str = AND_PAT.sub (', ', name_str)
	## Main:
	auth_list = name_str.split (', ')
	for i in range (len (auth_list)):
		single_auth = auth_list[i].strip()
		single_auth = single_auth.split (' ')
		family_name = single_auth[-1]
		if (family_name.endswith ('.')):
			family_name = family_name[:-1]
		given_names = ' '.join (single_auth[:-1])
		reverse_name = family_name
		if (given_names):
			reverse_name += ', ' + given_names
		auth_list[i] = reverse_name
	return auth_list



### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
