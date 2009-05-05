#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rename files as by the ISBN buried in their original name.

"""
# TODO: throttle parameter?
# TODO: Amazon query?
# TODO: output in other formats?

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import logging
import sys, re
from os import path, rename
from optparse import OptionParser
from exceptions import BaseException

from biblio.webquery import errors
from config import *
from common import *


### CONSTANTS & DEFINES ###

ISBN10_PAT = r'(\d{9}[\d|X])'
ISBN13_PAT = r'(\d{13})'

ISBN_PATS = [
	r'\(ISBN([^\)]+)\)',
	r'^(\d{13})$',
	r'^(\d{13})[\b|_|\.|\-|\s]',
	r'[\b|_|\.|\-|\s](\d{13})$',
	r'[\b|_|\.|\-|\s](\d{13})[\b|_|\.]',
	r'^(\d{9}[\d|X])$',
	r'^(\d{9}[\d|X])[\b|_|\.|\s|\-]',
	r'[\b|_|\.|\-|\s](\d{9}[\d|X])$',
	r'[\b|_|\.|\-|\s](\d{9}[\d|X])[\b|_|\.|\-|\s]',
	r'ISBN\s*(\d{13})',
	r'ISBN\s*(\d{9}[\d|X])',
	r'[\[\(](\d{9}[\d|X])[\]\)]',
	r'\D(\d{13})$',
	r'\D(\d{9}[\d|X])$',

]

ISBN_RE = [re.compile (p, re.IGNORECASE) for p in ISBN_PATS]

_DEV_MODE = True

DEF_NAME_FMT = '%(auth)s%(year)s_%(title)s_(isbn%(isbn)s)'
DEF_BLANK_CHARS = ''
STRIP_CHARS_RE = re.compile ('[\'\":\,!\.\?\(\)]')

COLLAPSE_SPACE_RE = re.compile (r'\s+')


CASE_CHOICES = {
	#'u':           'u',        
	'upper':       'u',
	#'uppercase':   'u',
	#'l':           'l',
	'lower':        'l',
	#'lowercase',
	#'o':            'o',
	'orig':         'o',
	#'original':     'o',
}


### IMPLEMENTATION ###

def parse_args():
	# Construct the option parser.
	usage = '%prog [options] FILES ...'
	version = "version %s" %  script_version
	epilog=''
	optparser = OptionParser (usage=usage, version=version, epilog=epilog)
	add_shared_options (optparser)

	optparser.add_option ('--case', '-c',
		dest='case',
		help="Whether to covert the case of the answer.",
		choices=sorted (CASE_CHOICES.keys()),
		default='orig',
	)
	
	optparser.add_option ('--leave_whitespace',
		action='store_false',
		dest='normalise_whitespace',
		help="Whether to clearup excess whitespace.",
		default=True,
	)
	
	optparser.add_option ('--replace_whitespace',
		dest='replace_whitespace',
		help="Replace whitespace with this character.",
		default=' ',
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
	
	optparser.add_option ('--unknown',
		dest='unknown',
		help="Use this string if value is undefined.",
		default='unknown',
	)
	
	# parse and check args
	options, fpaths = optparser.parse_args()
	
	if (not fpaths):
		optparser.error ('No files specified')
	check_shared_options (options)
	
	## Postconditions & return:
	return fpaths, options


def dir_base_ext_from_path (fpath):
	"""
	Return a files base name and extension from it's path.
	"""
	fdir, fname = path.split (fpath)
	base, ext = path.splitext (fname)
	return fdir, base, ext


def rename_file (oldpath, newname):
	"""
	Rename a file, while keeping it in the same location.
	"""
	fdir, fname = path.split (oldpath)
	newpath = path.join (fdir, newname)
	rename (oldpath, newpath)


def extract_isbn_from_filename (fname):
	for r in ISBN_RE:
		match = r.search (fname)
		if match:
			return match.group(1)
	return None
	

def generate_new_name (bibrec, options):
	if (bibrec.authors):
		primary_auth = bibrec.authors[0]
		auth_str = primary_auth.family or primary_auth.given
	else:
		auth_str = options.unknown
	logging.info ('~ found %s - %s' % (auth_str, bibrec.title))
	return DEF_NAME_FMT % {
		'auth': auth_str,
		'year': bibrec.year or options.unknown,
		'title': bibrec.short_title or options.unknown,
		'isbn': bibrec.id or options.unknown,
	}
	
	
def postprocess_name (name, options):
	## Preconditions:
	assert (name)
	## Main:
	name = STRIP_CHARS_RE.sub ('', name)
	# clean up excess whitespace
	if (options.normalise_whitespace):
		name = COLLAPSE_SPACE_RE.sub (' ', name.strip())
	if (options.replace_whitespace):
		name = name.replace (' ', options.replace_whitespace)
	# harmomise case
	if (options.case == 'lower'):
		name = name.lower()
	elif (options.case == 'upper'):
		name = name.upper()
	## Return:
	return name


def main():
	fpath_list, options = parse_args()
	logging.basicConfig (level=logging.INFO, stream=sys.stdout,
		format= "%(message)s")
	try:
		webqry = construct_webquery (options.webservice, options.service_key)
		for fpath in fpath_list:
			logging.info ('Original %s ...' % fpath)
			fdir, base, ext = dir_base_ext_from_path (fpath)
			isbn = extract_isbn_from_filename (base)
			logging.info ('~ extracted ISBN %s ...' % isbn)
			if (isbn):
				try:
					bibrec_list = webqry.query_bibdata_by_isbn (isbn,
						fmt='bibrecord')
					if (bibrec_list):
						bibinfo = bibrec_list[0]
						new_name = generate_new_name (bibinfo, options)
						new_name = postprocess_name (new_name, options)
						logging.info ('~ new name %s.' % new_name)
						newpath = path.join (fdir, new_name + ext)
						logging.info ('~ new path %s.' % newpath)
						rename_file = not (options.dryrun)
						if (path.exists (newpath)):
							logging.info ('~ path already exists')
							if not options.overwrite:
								rename_file = False
						if (rename_file):
							logging.info ('~ renaming file')
							rename (fpath, newpath)
					else:
						print "no records returned"
				except errors.QueryError, err:
					logging.info ('- query failed: %s.' % err)
			else:
				print "no isbn extracted"
		
	except BaseException, err:
		if (_DEV_MODE or options.debug):
			raise
		else:
			sys.exit (err)
	except:
		if (_DEV_MODE or option.debug):
			raise
		else:
			sys.exit ("An unknown error occurred.")
	
	
### TEST & DEBUG ###

### MAIN ###

if __name__ == '__main__':
	main()
	

### END ######################################################################
