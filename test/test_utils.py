#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for biblio.webquery.errors, using nose.
"""

### IMPORTS ###

from biblio.webquery import utils


### CONSTANTS & DEFINES ###

MULT_EDITORS = "K. Esser (Editor), U. Lüttge (Editor), W. Beyschlag (Editor), J. Murata (Editor)"


### TESTS ###

class test_parse_editing_info (object):
	def test_simple_str (self):
		pass
		
	def test_multiple_editors (self):
		e, s = utils.parse_editing_info (MULT_EDITORS)



### END ######################################################################
