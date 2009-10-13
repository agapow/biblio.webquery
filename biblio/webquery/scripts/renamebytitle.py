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

CLEAN_TITLE_RE = re.compile (r'[\-\._,]+')

DECAMEL_RE = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')

BRACKET_TMPL = r'\%(start)s[^\%(stop)s]*\%(stop)s'
BRACKET_CHARS = [
	[r'\(', r'\)'],
	[r'\[', r'\]'],
	[r'\{', r'\}']
]
BRACKET_RES = [re.compile (BRACKET_TMPL % {'start': x[0], 'stop': x[1]}) for
	x in BRACKET_CHARS]

REPLACE_CHARS = [
	r'\.',
	r'!',
	r'%20'
]
REPLACE_CHARS_RE = re.compile (r'|'.join (REPLACE_CHARS))

# remove edition info, isbns, publication year
STRIP_CHARS = [
	r'ebook\-een',
	r'(1st|2nd|3rd)\s+edition',
	r'isbn',
	r'[\d\- ]{10,}'
	r'[12]\d{3}'
]
STRIP_CHARS_RE = re.compile (r'|'.join (STRIP_CHARS))

COLLAPSE_SPACE_RE = re.compile (r'\s+')

_DEV_MODE = True

LOG_LEVELS = {
	0: logging.EXCEPTION,
	1: logging.CRITICAL,
	2: logging.ERROR,
	3: logging.WARNING,
	4: logging.INFO,
	5: logging.DEBUG,
}

### IMPLEMENTATION ###

def setup_global_logger (name='myscript', level=logging.INFO):
	global logger
	logging.basicConfig (level=level, stream=sys.stdout,
		format= "%(message)s")
	logger = logging.getLogger (name)

def partition_title (strn):
	"""
	Seperate the string into a title, author and other segment. 
	"""
	if (' by ' in strn):
		return [x.strip() for x in strn.split (' by ', 1)]
	#for sep in ['-', '_', ':']

def ask_choice (prompt="Your choice", choices='yna',
		transform=lambda s: s.lower()):
	"""
	Prompt the user for a choice.
	
	:Parameters:
		prompt
			The message to prompt the user 
	
	The choices can be a string (of 1 letter choices) or a list of strings.
	The prompt will repeat until a legal answer is given.
	
	"""
	# TODO: a transform input param, to map or cleanup input?
	print "%s? [%s]" % (prompt, ','.join (list (choices))),
	answer = transform (raw_input().strip())
	if (answer in choices):
		return answer
	else:
		return ask_choice (prompt, choices)
	
	
def decamel (stringAsCamelCase):
	"""
	Converts a string with camelCaseWords to a space delimited one.
	
	For example::
	
		>>> decamel ('Magic fun Time hurray')
		'Magic fun Time hurray'
		>>> decamel ('Magic funTime hurray')
		'Magic fun Time hurray'
		>>> decamel ('Magic FunTime hurray')
		'Magic Fun Time hurray'
		>>> decamel ('MagicFun funTimeHurray')
		'Magic Fun fun Time Hurray'
		
	"""
	if stringAsCamelCase is None:
		return None
	return DECAMEL_RE.sub (lambda m: m.group()[:1] + " " + m.group()[1:], stringAsCamelCase)
		
		
def strip_asides (strn):
	"""
	Remove bracketed sections from string.
	
	For example::
	
		>>> strip_asides ('This is (not) funny.')
		'This is  funny.'
		>>> strip_asides ('This is funny.')
		'This is funny.'
		>>> strip_asides ('This [is] (not) funny.')
		'This   funny.'
		>>> strip_asides ('This [is (not) funny].')
		'This .'
		
	"""
	for re in BRACKET_RES:
		strn = re.sub (' ', strn)
	return strn
	
def replace_chars (strn):
	"""
	Replace various substrings with a space.
	"""
	return REPLACE_CHARS_RE.sub (' ', strn)
	
def strip_chars (strn):
	"""
	Replace various substrings with a space.
	"""
	return STRIP_CHARS_RE.sub ('', strn)
	
def norm_space (strn):
	"""
	Cleanup space in a string.
	"""
	return COLLAPSE_SPACE_RE.sub (' ', strn).strip()
		
	
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
	# clean up name
	basename = fname
	logger.debug ("Basename %s ..." % basename)
	basename = decamel (basename).lower()
	logger.debug ("Decamel'd %s ..." % basename)
	basename = strip_asides (basename)
	logger.debug ("No asides %s ..." % basename)
	basename = strip_chars (basename)
	logger.debug ("Strip chars %s ..." % basename)
	basename = replace_chars (basename)
	logger.debug ("Replace chars %s ..." % basename)
	basename = norm_space (basename)
	logger.debug ("Cleanup space %s ..." % basename)
	
	# break into parts
	if (' by ' in basename):
		parts = basename.split ( ' by ')

	# TODO: check for 'by'
#	for re in STRIP_TITLE_RES:
#		stripped_name = re.sub ('', stripped_name)
#	splitchar = ''
#	for c in ['-', '_', '.']:
#		if stripped_name.count(c):
#			splitchar = c
#			break
#	if (splitchar):
#		part1, part2 = stripped_name.split (splitchar, 1)
#		part1 = CLEAN_TITLE_RE.sub (' ', part1).strip()
#		part2 = CLEAN_TITLE_RE.sub (' ', part2).strip()
#		wordlen1, wordlen2 = len (part1.split (' ')), len (part2.split (' '))
#		if (wordlen2 < wordlen1):
#			title = part1
#		else:
#			title = part2
#	else:
#		title = stripped_name
#	clean_title = CLEAN_TITLE_RE.sub (' ', title).strip()
#	return clean_title

	return basename


def main():
	fpath_list, options = parse_args()
	setup_global_logger ('renamebytitle', logging.DEBUG)

	try:
		webqry = construct_webquery (options.webservice, options.service_key)
		for fpath in fpath_list:
			logger.info ("Original %s ..." % fpath)
			fdir, base, ext = dir_base_ext_from_path (fpath)
			title = extract_title_from_filename (base)
			logger.info ("~ extracted title '%s' ..." % title)
			continue
			if (isbn):
				try:
					bibrec_list = webqry.query_bibdata_by_isbn (isbn,
						format='bibrecord')
					if (bibrec_list):
						bibinfo = bibrec_list[0]
						new_name = generate_new_name (bibinfo, options)
						new_name = postprocess_name (new_name, options)
						logger.info ('~ new name %s' % new_name)
						newpath = path.join (fdir, new_name + ext)
						logger.info ('~ new path %s' % newpath)
						rename_file = not (options.dryrun)
						if (path.exists (newpath)):
							logger.info ('~ path already exists')
							if not options.overwrite:
								rename_file = False
						if (rename_file):
							logger.info ('~ renaming file')
							rename (fpath, newpath)
					else:
						logger.info ('- no records returned')
				except errors.QueryError, err:
					logger.info ('- query failed: %s.' % err)
			else:
				print logger.info ('- no isbn extracted')
		
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

def _doctest ():
	import doctest
	doctest.testmod()
	

### MAIN ###

if __name__ == '__main__':
	main()
	

### END ######################################################################
