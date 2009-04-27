#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Querying WorldCat xISBN service for bibliographic information and normalising the results.

"""
# TODO: error-handling logic is correct?

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import re
try: 
	from xml.etree import ElementTree
except:
	from elementtree import ElementTree

from basewebquery import BaseWebquery


### CONSTANTS & DEFINES ###

XISBN_ROOTURL = 'http://xisbn.worldcat.org/webservices/xid/isbn/'

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

FORMATS = [
	'raw',
	'xml',
#	'html',
#	'json',
#	'python',
#	'ruby',
#	'php',
#	'csv',
#	'txt',
]


### IMPLEMENTATION ###

class XisbnQuery (BaseWebquery):
	
	def __init__ (self, timeout=5.0, limits=None):
		"""
		C'tor.
		"""
		BaseWebquery.__init__ (self, root_url=XISBN_ROOTURL, timeout=5.0,
			limits=None)
		
	def query_mdata_by_isbn (self, isbn, fmt='xml'):
		"""
		Return publication data based on ISBN.
		
		:Parameters:
			isbn : string
				An ISBN-10 or ISBN-13.
				
		:Returns:
			Publication data in Xisbn XML format.
		
		"""
		isbn = impl.normalize_isbn (isbn)
		sub_url = '%(isbn)s?method=getMetadata&format=xml&fl=*' % {'isbn': isbn}
		return self.query (sub_url)

	def isbn10_to_isbn13 (self, isbn, fmt='xml'):
		isbn = impl.normalize_isbn (isbn)
		sub_url = '%(isbn)s?method=to13&format=xml' % {'isbn': isbn}
		
		
		
	
def xisbn_metadata_xml_to_bibrecord (xml_txt):
	"""
	Translate the XML returned by xISBN to a BibRecord.
	
	:Parameters:
		mdata_xml : string
			An Xisbn record in XML.
			
	:Returns:
		A dictionary with keys "year", "title" and "authors" parsed from the 
		Xisbn record. If a field is not present or parseable, neither is
		the key.
		
	"""
	## Main:
	# capture in etree and find record node
	tree = ElementTree.fromstring (mdata_xml)
	isbn_elem = tree.find ('{http://worldcat.org/xid/isbn/}isbn')
	# parse individual fields
	fields = {}
	if (isbn_elem is not None):
		year = isbn_elem.get ('year')
		if (year):
			fields['year'] = year
		title = isbn_elem.get ('title')
		if (title):
			fields['title'] = parse_title (title)
		author = isbn_elem.get ('author')
		if (author):
			fields['authors'] = parse_authors (author)
	## Postconditions & return:
	return fields


def parse_xisbn_authors (auth_str):
	"""
	Clean up Xisbn author information into a more consistent format.

	:Parameters:
		auth_str : string
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
	auth_str = auth_str.strip()
	if (not auth_str):
		return []
	# strip extraneous and replace 'and'
	for pat in STRIP_PATS:
		auth_str = pat.sub ('', auth_str)
	auth_str = AND_PAT.sub (', ', auth_str)
	## Main:
	auth_list = auth_str.split (', ')
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
