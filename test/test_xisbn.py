#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for biblio.webquery.xisbn, using nose.
"""

### IMPORTS ###

from biblio.webquery import xisbn


### CONSTANTS & DEFINES ###

BAD_STATUS_XML = """<?xml version="1.0" encoding="UTF-8" ?>
	<rsp xmlns="http://worldcat.org/xid/isbn/" stat="invalidId"/>"""

SIMPLE_ONE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rsp xmlns="http://worldcat.org/xid/isbn/" stat="ok">
	<isbn title="Learning Python" form="BA" year="2004" lang="eng" ed="2nd ed." author="Lutz, Mark." publisher="O'Reilly">0596002815</isbn>
</rsp>"""


### TESTS ###

class xtest_xisbn_xml_to_dicts (object):
	def test_bad_status (self):
		try:
			recs = xisbn.xisbn_xml_to_dicts (BAD_STATUS_XML)
			assert (False), "should fail if reading document with bad status"
		except:
			pass

	def test_simple_one (self):
		recs = xisbn.xisbn_xml_to_dicts (SIMPLE_ONE_XML)




### END ######################################################################
