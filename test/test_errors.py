#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for biblio.webquery.errors, using nose.
"""

### IMPORTS ###

import time

from biblio.webquery import errors


### CONSTANTS & DEFINES ###

### TESTS ###

def test_querythrottleerror():
	# just see it gives msg correctly
	err = errors.QueryThrottleError ('my msg')
	assert (str (err) == 'my msg')
	try:
		raise err
	except errors.QueryThrottleError, ex:
		assert (str (err) == 'my msg')
	except:
		assert (False), "error should be caught elsewhere"



### END ######################################################################
