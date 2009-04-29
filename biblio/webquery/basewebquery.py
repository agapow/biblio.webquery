#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A base class for querying webservices.
"""
# TODO: list of possibel apis at http://techessence.info/apis and
# http://www.programmableweb.com/apitag/books#


__docformat__ = 'restructuredtext en'


### IMPORTS ###

import socket
from urllib import urlopen, quote

import impl


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###

class BaseWebquery (impl.ReprObj):
	"""
	A base class for querying webservices.
	
	This serves as a foundation for other web-query classes, centralising a
	small amount of functionality and providing a common interface. Over time,
	the services provided here will probably expand.
	
	"""
	
	_repr_fields = [
		'root_url',
		'timeout',
		'limits',
	]
	
	def __init__ (self, root_url, timeout=5.0, limits=[]):
		"""
		Ctor, allowing the setting of the webservice, timeout and limits on use.
		"""
		self.root_url = root_url
		self.timeout = timeout
		self.limits = []
		for ql in list (limits):
			self.limits.append (ql)

	def query (self, url):
		for limit in self.limits:
			limit.check_limit (self)
		socket.setdefaulttimeout (self.timeout)
		full_url = self.root_url + url
		return urlopen (full_url).read()


class BaseKeyedWebQuery (BaseWebquery):
	"""
	A Webquery that requires an access key.
	"""
	def __init__ (self, root_url, key, timeout=5.0, limits=[]):
		"""
		Ctor, allowing the setting of a webservice access key.
		"""
		BaseWebquery.__init__ (self, root_url=root_url, timeout=timeout,
			limits=limits)
		self.key = key
			

	
### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
