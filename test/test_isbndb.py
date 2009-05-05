#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for biblio.webquery.isbndb, using nose.
"""

### IMPORTS ###

from biblio.webquery import isbndb


### CONSTANTS & DEFINES ###

BAD_STATUS_XML = """<?xml version="1.0" encoding="UTF-8" ?>
	<rsp xmlns="http://worldcat.org/xid/isbn/" stat="invalidId"/>"""

SIMPLE_ONE_XML = """<?xml version="1.0" encoding="UTF-8"?>
	<ISBNdb server_time="2005-07-29T02:41:22">
	 <BookList total_results="1" page_size="10" page_number="1" shown_results="1">
	  <BookData book_id="law_and_disorder" isbn="0210406240">
	   <Title>Law and disorder</Title>
	   <TitleLong>
	    Law and disorder: law enforcement in television network news
	   </TitleLong>
	   <AuthorsText>V. M. Mishra</AuthorsText>
	   <PublisherText publisher_id="asia_pub_house">
	    New York: Asia Pub. House, c1979.
	   </PublisherText>
	   <Details dewey_decimal="302.2/3"
	            dewey_decimal_normalized="302.23"
	            lcc_number="PN4888"
	            language="eng"
	            physical_description_text="x, 127 p. ; 22 cm."
	            edition_info=""
	            change_time="2004-10-19T23:52:56"
	            price_time="2005-07-29T02:06:41" />
	  </BookData>
	 </BookList>
	</ISBNdb>"""


### TESTS ###

class test_isbndb_xml_to_bibrecords (object):
	#def test_bad_status (self):
	#	try:
	#		recs = xisbn.xisbn_xml_to_dicts (BAD_STATUS_XML)
	#		assert (False), "should fail if reading document with bad status"
	#	except:
	#		pass

	def test_simple_one (self):
		recs = isbndb.isbndb_xml_to_bibrecords (SIMPLE_ONE_XML)
		assert (len (recs) == 1)




### END ######################################################################
