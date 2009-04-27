#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various errors thrown by the the module.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import exceptions


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###

class NoResults (exceptions.ValueError):
	"""
	Thrown when parsing results with no results.
	"""
	
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
		

### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
