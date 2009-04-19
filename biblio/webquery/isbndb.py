#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Querying the ISBNDb for bibliographic information.
"""
# TODO: error-handling logic is correct?

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from basewebquery import BaseWebquery
import querythrottle


### CONSTANTS & DEFINES ###

ISBNDB_ROOTURL = 'http://isbndb.com/api/books.xml?access_key=%(key)s'
ISBNDB_KEY = 'OPNH8HG2'


### IMPLEMENTATION ###

class IsbndbQuery (BaseWebquery):
	
	def __init__ (self, key=ISBNDB_KEY):
		"""
		C'tor, accepting an access key.
		"""
		root_url = ISBNDB_ROOTURL % {'key': key}
		BaseWebquery.__init__ (self, root_url=root_url, \
			limits=[querythrottle.OncePerSecondThrottleLimit()])
		
	def query_mdata_by_isbn (self, isbn):
		"""
		Return the metadata for a publication specified by ISBN.
		"""
		sub_url = '&results=authors,subjects,texts&index1=isbn'\
			'&value1=%(isbn)s' % {'isbn': isbn}
		return self.query (sub_url)




### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
