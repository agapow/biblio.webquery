#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for biblio.webquery.worldcat, using nose.
"""

### IMPORTS ###



### CONSTANTS & DEFINES ###

### TESTS ###

def test_parse_authors():
	test_dict = {
		"edited by Carol Shoshkes Reiss.":
			['Reiss, Carol Shoshkes'],
		"by Bill Scott, Theresa Neil." :
			['Scott, Bill', 'Neil, Theresa'],
		"Leonard Richardson and Sam Ruby.":
			['Richardson, Leonard', 'Ruby, Sam'], 
		"Huntington F. Willard and Geoffrey S. Ginsburg.":
			['Willard, Huntington F.', 'Ginsburg, Geoffrey S.'],
		"edited by Steven Laureys, Giulio Tononi.":
			['Laureys, Steven', 'Tononi, Giulio'],
		"Jack D. Edinger, Colleen E. Carney.":
			['Edinger, Jack D.', 'Carney, Colleen E.'],
		"Ann Thomson.":
			['Thomson, Ann'],
		"[John Grossman]":
			['Grossman, John'],
		"Stephen P. Schoenberger, Bali Pulendran, editors.":
			['Schoenberger, Stephen P.', 'Pulendran, Bali'],
		"Philip J. Davis, Reuben Hersh ; with an introduction by Gian-Carlo Rota.":
			['Davis, Philip J.', 'Hersh, Reuben'],
		"Madonna": ['Madonna'],
	}
	for k, v in test_dict.iteritems():
		assert (worldcat.parse_authors (k) == v)



### END ######################################################################
