#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various errors thrown by the the module.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import exceptions

__all__ = [
	'NoResultsError',
	'ParseError',
	'QueryThrottleError',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###

class NoResultsError (exceptions.ValueError):
	"""
	Thrown when parsing results with no results.
	"""
	
	def __init__ (self, msg):
		"""
		C'tor.
		"""
		exceptions.ValueError (self, msg)
		

class ParseError (exceptions.ValueError):
	"""
	Thrown when parsing webservice formats.
	"""
	
	def __init__ (self, msg):
		"""
		C'tor.
		"""
		exceptions.ValueError (self, msg)
		

class QueryThrottleError (exceptions.RuntimeError):
	"""
	An exception to throw when a query limit has been exceeded.
	
	It serves little purpose except to distinguish failures caused by exceeding
	query limits.
	
	"""
	def __init__ (self, msg=None):
		msg = msg or "query limit exceeded"
		RuntimeError.__init__ (self, msg)



### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
