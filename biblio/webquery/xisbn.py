#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Querying WorldCat xISBN service for bibliographic information and normalising the results.

"""
# TODO: error-handling logic is correct?

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import re

from impl import ElementTree
from basewebquery import BaseWebquery


### CONSTANTS & DEFINES ###

XISBN_ROOTURL = 'http://xisbn.worldcat.org/webservices/xid/isbn/'



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
		
	def query_bibdata_by_isbn (self, isbn, fmt='xml'):
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

	def query_isbn10_to_13 (self, isbn, fmt='xml'):
		isbn = impl.normalize_isbn (isbn)
		sub_url = '%(isbn)s?method=to13&format=xml' % {'isbn': isbn}
		
		
		
	
def xisbn_pytxt_to_bibrecord (pytxt):
	"""
	Translate the Python text returned by xISBN to a BibRecord.
	
	:Parameters:
		mdata_xml : string
			An Xisbn record in XML.
			
	:Returns:
		A dictionary with keys "year", "title" and "authors" parsed from the 
		Xisbn record. If a field is not present or parseable, neither is
		the key.
		
	"""
	## Main:
	# convert to python structures
	xisbn_dict = eval (pytxt)
	# parse reply
	status = xisbn_dict.get ('stat', 'ok')
	assert (status == 'ok'), "reponse status was bad (%s)" % status
	# parse individual records
	bibrecs = []
	for entry in xisbn_dict['list']:
		new_bib = BibRecord()
		new_bib.publisher = entry.get ('publisher', '')
		new_bib.lang = entry.get ('lang', '')
		new_bib.pubcity = entry.get ('city', '')
		new_bib.author = entry.get ('author', '')
		new_bib.pubyear = entry.get ('year', '')
		new_bib.key = entry.get ('isbn', [''])[0]
		new_bib.title = entry.get ('title', '')
		bibrecs.append (new_bib)
	## Postconditions & return:
	return fields


def xisbn_pytxt_to_dicts (xml_txt):
	"""
	Translate the python text returned by xISBN to a series of dicts.
	
	:Parameters:
		mdata_xml : string
			An Xisbn record in XML.
			
	:Returns:
		A dictionary with keys "year", "title" and "authors" parsed from the 
		Xisbn record. If a field is not present or parseable, neither is
		the key.
		
	"""
	## Preconditions & preparation:
	# find root and check status
	root = ElementTree.fromstring (xml_txt)
	print xml_txt
	print root.tag
	assert (root.tag == '{http://worldcat.org/xid/isbn/}rsp'), \
		"expected xISBN XML document to have root 'rsp' not '%s'" % root.tag
	print root.attrib['stat']
	assert (root.attrib['stat'] == 'ok'), "webservice returned '%s'" % root.attrib['stat']
	## Main:
	isbn_dicts = []
	for child in root:
		rec_dict = {}
		rec_dict['isbn'] = child.text
		

		isbn_dicts.append (rec_dict)
	return isbn_dicts

	isbn_elem = tree.find ('isbn')
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



### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
