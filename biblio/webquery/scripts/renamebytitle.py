#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rename files as by the title buried in their original name.

"""

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

DIVID_CHARS = ['-', '_', ',', '.']

CLEAN_TITLE_RE = re.compile (r'[\-\._,]+')
STRIP_TITLE_RES = [re.compile (p) for p in [
		r'\([^\)]*\)',
		r'\[[^\]]*\)',
		r'\d{5,}$',
		r'[\-\._\s,]+$',
		r'^[\-\._\s,]',
		r'\s*(1st|2nd|3rd)\s+edition$',
	]
]

DECAMEL_RE = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')

_DEV_MODE = True


### IMPLEMENTATION ###

def ask_choice (prompt="Use this", choices='yna'):
	print "%s? [%s]" % (prompt, choices),
	answer = raw_input().lower().strip()
	if (answer in choices):
		return answer
	else:
		return ask_choice (prompt, choices)
	
def space_out_camel_case(stringAsCamelCase):
	"""Adds spaces to a camel case string.Failure to space out string returns the original string.
	>>> space_out_camel_case('DMLSServicesOtherBSTextLLC')
	'DMLS Services Other BS Text LLC'
	"""
	if stringAsCamelCase is None:
		return None
	return DECAMEL_RE.sub (lambda m: m.group()[:1] + " " + m.group()[1:], stringAsCamelCase)
		
	
def parse_args():
	# Construct the option parser.
	usage = '%prog [options] FILES ...'
	version = "version %s" %  script_version
	description='Extract an title from a file name, look up the associated ' \
		'bibliographic information in a webservice and rename the file ' \
		'appropriately.'
	epilog='Titles are extracted from filenames by pure heuristics - obviously ' \
		'not all forms will be found. ' \
		'The new name is generated first before the various processing ' \
		'options are applied. In order, characters are stripped from the ' \
		'name, excess whitespace is collapsed and then the case conversion ' \
		'is applied. The file extension, if any, is removed before renaming ' \
		'and re-applied afterwards. ' \
		'We suggest you try a dryrun before renaming any files.'
	optparser = OptionParser (usage=usage, version=version, epilog=epilog,
		description=description)
	add_shared_options (optparser)
	add_renaming_options (optparser)
	
	# parse and check args
	options, fpaths = optparser.parse_args()
	
	if (not fpaths):
		optparser.error ('No files specified')
	check_shared_options (options, optparser)
	
	## Postconditions & return:
	return fpaths, options


def dir_base_ext_from_path (fpath):
	"""
	Return a files base name and extension from it's path.
	"""
	fdir, fname = path.split (fpath)
	base, ext = path.splitext (fname)
	return fdir, base, ext


def rename_inplace (oldpath, newname):
	"""
	Rename a file, while keeping it in the same location.
	"""
	fdir, fname = path.split (oldpath)
	newpath = path.join (fdir, newname)
	rename (oldpath, newpath)


def extract_title_from_filename (fname):
	# TODO: check for 'by'
	stripped_name = space_out_camel_case (fname).strip().lower()
	for re in STRIP_TITLE_RES:
		stripped_name = re.sub ('', stripped_name)
	splitchar = ''
	for c in ['-', '_', '.']:
		if stripped_name.count(c):
			splitchar = c
			break
	if (splitchar):
		part1, part2 = stripped_name.split (splitchar, 1)
		part1 = CLEAN_TITLE_RE.sub (' ', part1).strip()
		part2 = CLEAN_TITLE_RE.sub (' ', part2).strip()
		wordlen1, wordlen2 = len (part1.split (' ')), len (part2.split (' '))
		if (wordlen2 < wordlen1):
			title = part1
		else:
			title = part2
	else:
		title = stripped_name
	clean_title = CLEAN_TITLE_RE.sub (' ', title).strip()
	return clean_title


def main():
	fpath_list, options = parse_args()
	logging.basicConfig (level=logging.INFO, stream=sys.stdout,
		format= "%(message)s")
	try:
		webqry = construct_webquery (options.webservice, options.service_key)
		for fpath in fpath_list:
			logging.info ("Original %s ..." % fpath)
			fdir, base, ext = dir_base_ext_from_path (fpath)
			title = extract_title_from_filename (base)
			logging.info ("~ extracted title '%s' ..." % title)
			continue
			if (isbn):
				try:
					bibrec_list = webqry.query_bibdata_by_isbn (isbn,
						format='bibrecord')
					if (bibrec_list):
						bibinfo = bibrec_list[0]
						new_name = generate_new_name (bibinfo, options)
						new_name = postprocess_name (new_name, options)
						logging.info ('~ new name %s' % new_name)
						newpath = path.join (fdir, new_name + ext)
						logging.info ('~ new path %s' % newpath)
						rename_file = not (options.dryrun)
						if (path.exists (newpath)):
							logging.info ('~ path already exists')
							if not options.overwrite:
								rename_file = False
						if (rename_file):
							logging.info ('~ renaming file')
							rename (fpath, newpath)
					else:
						logging.info ('- no records returned')
				except errors.QueryError, err:
					logging.info ('- query failed: %s.' % err)
			else:
				print logging.info ('- no isbn extracted')
		
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
