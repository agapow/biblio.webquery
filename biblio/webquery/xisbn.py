#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Querying WorldCat xISBN service for bibliographic information and normalising the results.

"""
# TODO: error-handling logic is correct?

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import re

from impl normalize_isbn
from basewebquery import BaseWebquery
from bibrecord import BibRecord

__all__ = [
	'XisbnQuery',
	'xisbn_py_to_bibrecord',
]


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

	def query_service (self, isbn, method, format, fields=['*']):
		sub_url = "%(isbn)s?method=%(mthd)s&format=%(fmt)s&fl=%(flds)s" % {
			'mthd': method,
			'fmt': format,
			'isbn': normalize_isbn (isbn),
			'flds': ','.join (fields),
		}
		return self.query (sub_url)
		
	def query_bibdata_by_isbn (self, isbn, fmt='bibrecord'):
		"""
		Return publication data based on ISBN.
		
		:Parameters:
			isbn : string
				An ISBN-10 or ISBN-13.
				
		:Returns:
			Publication data in Xisbn XML format.
		
		"""
		## Preconditions & preparation:
		# clean up params, check and select appropriate format
		fmt_map = {
			'python':      'python',
			'xml':         'xml',
			'bibrecord':   'python',
		}
		assert (fmt in fmt_map), \
			"unrecognised format '%s', must be one of %s" % (fmt, fmt_map.keys())
		## Main:
		passed_fmt = fmt_map[fmt]
		results = self.query_service (isbn=isbn, method='getMetadata',
			format=passed_fmt)
		if (fmt == 'bibrecord'):
			results = xisbn_py_to_bibrecord (results)
		## Postconditions & return:
		return results

	def query_isbn10_to_13 (self, isbn, fmt='xml'):
		isbn = normalize_isbn (isbn)
		sub_url = '%(isbn)s?method=to13&format=xml' % {'isbn': isbn}
		
		
		
	
def xisbn_py_to_bibrecord (pytxt):
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
	return bibrecs



### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
