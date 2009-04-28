#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Querying the ISBNDb for bibliographic information.
"""
# TODO: error-handling logic is correct?

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from impl import ElementTree
from basewebquery import BaseWebquery


### CONSTANTS & DEFINES ###

ISBNDB_ROOTURL = 'http://isbndb.com/api/books.xml?access_key=%(key)s'
ISBNDB_KEY = 'OPNH8HG2'

FORMATS = [
	'isbndb-xml',
	'bibrecord',
]


### IMPLEMENTATION ###

class IsbndbQuery (BaseWebquery):
	
	def __init__ (self, key=ISBNDB_KEY, timeout=5.0, limits=None):
		"""
		C'tor, accepting an access key.
		"""
		root_url = ISBNDB_ROOTURL % {'key': key}
		BaseWebquery.__init__ (self, root_url=root_url, timeout=timeout,
			limits=limits)
		
	def query_bibdata_by_isbn (self, isbn, fmt='isbn-xml'):
		"""
		Return the metadata for a publication specified by ISBN.
		"""
		sub_url = '&results=authors,subjects,texts,details&index1=isbn'\
			'&value1=%(isbn)s' % {'isbn': isbn}
		results = self.query (sub_url)
		if (fmt is 'bibrecord'):
			results = isbndb_booklist_to_bibrecords (results)
		return results


def isbndb_booklist_to_bibrecords (xml_txt):
	tree = ElementTree.fromstring (xml_txt)
	root = tree.root
	assert_or_raise (root.tag == 'ISBNdb', errors.ParseError,
		"ISBNdb document root should be 'ISBNdb', not '%s'" % root.tag)
	assert_or_raise (len (root) == 1, errors.ParseError,
		"ISBNdb document root has wrong number of children (%s)" % len (root))
	booklist_elem = root
	assert_or_raise (booklist_elem.tag == 'BookList', errors.ParseError,
		"ISBNdb document should contain 'BookList', not '%s'" % booklist_elem.tag)
	bibrecs = []
	for bdata in booklist_elem.findall ('BookData'):
		newrec = BibRecord()
		newrec.pubtype = 'book'
		new_rec.title = (bdata.findtext ('TitleLong') or u'').strip()
		newrec.abstract = (bdata.findtext ('Summary') or u'').strip()
		newrec.note = (bdata.findtext ('Notes') or u'').strip()
		newrec.keywords = [e.text.strip() for e in bdata.findall ('Subject')]
		author_elem = bdata.find ('Authors')
		newrec.authors = [e.text.strip() for e in author_elem.findall ('Person')]
		self.bibkey = bdata['isbn']
		self.publisher = u''
		self.pubyear = None
		self.edited = False


def parse_isbndb_person (txt):
	"""
	Attempt to convert the ISBNdb representation of a name into a canonical form.
	"""
	pass


def parse_isbndb_publisher (txt):
	"""
	Attempt to convert the ISBNdb representation of a name into a canonical form.
	"""
	pass


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
