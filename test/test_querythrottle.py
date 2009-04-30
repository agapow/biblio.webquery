#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for biblio.webquery.querythrottle, using nose.
"""

### IMPORTS ###

import time

from biblio.webquery import querythrottle


### CONSTANTS & DEFINES ###

### TESTS ###

def test_waitonfail():
	# use WaitNSecondsThrottle to test fail behaviour
	throttle = querythrottle.WaitNSecondsThrottle (0.3)
	# should immediately be okay
	start_time = time.time()
	throttle.check_limit (None)
	new_time = time.time()
	assert ((new_time - start_time) < 0.1)
	# should wait for rest of period
	throttle.check_limit (None)
	last_time = time.time()
	assert (0.3 < (last_time - new_time))


def test_raiseonfail():
	# use WaitNSecondsThrottle to test fail behaviour
	throttle = querythrottle.WaitNSecondsThrottle (0.3,
		querythrottle.FAIL_AND_RAISE)
	# should immediately be okay
	start_time = time.time()
	throttle.check_limit (None)
	new_time = time.time()
	assert ((new_time - start_time) < 0.1)
	# should throw since we can't fulfil
	try:
		throttle.check_limit (None)
		assert ("shouldn't get here")
	except:
		pass
		

def test_waitnsecondsthrottle():
	# check timing works
	throttle = querythrottle.WaitNSecondsThrottle (0.4)
	# should immediately be okay
	assert (throttle.within_limit (None))
	throttle.log_success (None)
	# should be locked down and return false just after success
	assert (not throttle.within_limit (None))
	time.sleep (0.2)
	# shiould still be false, as still within limit
	assert (not throttle.within_limit (None))
	time.sleep (0.3)
	# should have reset by now
	assert (throttle.within_limit (None))


def test_waitonesecondthrottle():
	# check timing works
	throttle = querythrottle.WaitOneSecondThrottle()
	# should immediately be okay
	assert (throttle.within_limit (None))
	throttle.log_success (None)
	# should be locked down and return false for rest of period
	assert (not throttle.within_limit (None))
	time.sleep (0.9)
	assert (not throttle.within_limit (None))
	time.sleep (0.2)
	assert (throttle.within_limit (None))


def test_absolutenumberthrottle():
	throttle = querythrottle.AbsoluteNumberThrottle (5)
	for i in range (5):
		assert (throttle.within_limit (None))
		throttle.log_success (None)
	assert (not throttle.within_limit (None))
	throttle = querythrottle.AbsoluteNumberThrottle (5)
	for i in range (5):
		throttle.check_limit (None)
	try:
		throttle.check_limit (None)
		assert ("shouldn't get here")
	except:
		pass



### END ######################################################################
