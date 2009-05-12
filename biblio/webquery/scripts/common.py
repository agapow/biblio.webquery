#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function shared between the scripts.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import re

from biblio.webquery.basewebquery import *
from config import *

try:
	from biblio.webquery import __version__ as script_version
except:
	script_version = 'unknown'

__all__ = [
	'script_version',
	'add_shared_options',
	'check_shared_options',
	'construct_webquery',
	'add_renaming_options',
]


### CONSTANTS & DEFINES ###

DEF_NAME_FMT = '%(auth)s%(year)s_%(short_title)s_isbn%(isbn)s'
DEF_STRIP_CHARS = ''':!,'".?()'''
DEF_BLANK_CHARS = '/\\'
STRIP_CHARS_RE = re.compile ('[\'\":\,!\.\?\(\)]')
COLLAPSE_SPACE_RE = re.compile (r'\s+')


CASE_CHOICES = [
	'orig',
	'upper',
	'lower',
]


### IMPLEMENTATION ###

def add_shared_options (optparser):
	optparser.add_option ('--debug',
		dest="debug",
		action='store_true',
		help='For errors, issue a full traceback instead of just a message.',
	)
	
	optparser.add_option ('--service', '-s',
		dest='webservice',
		help="The webservice to query. Choices are %s. The default is %s." % (
			', '.join (['%s (%s)' % (s['id'], s['title']) for s in WEBSERVICES]),
			DEFAULT_WEBSERVICE['id']
		) ,
		metavar='SERVICE',
		choices=WEBSERVICE_LOOKUP.keys(),
		default=DEFAULT_WEBSERVICE['id'],
	)
	
	optparser.add_option ('--key', '-k',
		dest="service_key",
		help='''The access key for the webservice, if one is required.''',
		metavar='KEY',
		default=None,
	)


def check_shared_options (options, optparser):
	serv = WEBSERVICE_LOOKUP.get (options.webservice, None)
	if (not serv):
		optparser.error ("Unrecognised webservice '%s'" % options.webservice)
	if (issubclass (serv['ctor'], BaseKeyedWebQuery)):
		if (not options.service_key):
			optparser.error ("%s webservice requires access key" % serv['title'])
	else:
		if (options.service_key):
			optparser.error ("%s webservice does not require access key" %
				serv['title'])


def add_renaming_options (optparser):
	optparser.add_option ('--case', '-c',
		dest='case',
		help="Case conversion of the new file name. Choices are %s." \
			"The default is %s. " % (', '.join (CASE_CHOICES), CASE_CHOICES[0]),
		choices=CASE_CHOICES,
		default=CASE_CHOICES[0],
	),
	
	optparser.add_option ('--leave_whitespace',
		action='store_true',
		dest='leave_whitespace',
		help="Leave excess whitespace. By default, consecutive spaces in " \
			"names are compacted",
		default=False,
	)
	
	optparser.add_option ('--replace_whitespace',
		dest='replace_whitespace',
		help="Replace whitespace in the new name with this string.",
		default='',
	)
	
	optparser.add_option ('--strip_chars',
		dest='strip_chars',
		help="Remove these characters from the new name. By default " \
			"they are '%s'." % DEF_STRIP_CHARS,
		default=DEF_STRIP_CHARS,
	)
	
	optparser.add_option ('--space_chars',
		dest='space_chars',
		help="Replace these characters in the new name with a space. By default " \
			"they are '%s'." % DEF_BLANK_CHARS,
		default=DEF_BLANK_CHARS,
	)
	
	optparser.add_option ('--overwrite',
		action='store_true',
		dest='overwrite',
		help="Overwrite existing files.",
		default=False,
	)
	
	optparser.add_option ('--dryrun',
		action='store_true',
		dest='dryrun',
		help="Check function and without renaming files.",
		default=False,
	)
	
	optparser.add_option ('--template',
		dest='template',
		help="The form to use for renaming the file. The fields recognised are " \
			"auth (primary authors family name), " \
			"title (full title of the book), " \
			"short_title (abbreviated title), " \
			"isbn, " \
			"year (year of publication). The default is '%s'." % DEF_NAME_FMT,
		default=DEF_NAME_FMT,
	)
	
	optparser.add_option ('--unknown',
		dest='unknown',
		help="Use this string if value is undefined.",
		default='unknown',
	)


def construct_webquery (service, key):
	serv_cls = WEBSERVICE_LOOKUP[service]['ctor']
	if (issubclass (serv_cls, BaseKeyedWebQuery)):
		return serv_cls (key=key, timeout=5.0, limits=None)
	else:
		return serv_cls (timeout=5.0, limits=None)

	
	
### TEST & DEBUG ###

### MAIN ###

if __name__ == '__main__':
	main()
	

### END ######################################################################
