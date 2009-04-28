#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Retreive bibliographic information for a given ISBN.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import sys
from os import path, rename
from optparse import OptionParser
from exceptions import BaseException

try:
	from biblio.webquery import __version__
except:
	__version__ = 'unknown'
	

### CONSTANTS & DEFINES ###

DEFAULT_NAME_FMT = '%(auth)s %(year)s %(title)s %(isbn)s'

SERVICE_LIST = [
	#abbrev       module
	['loc',        'loc',         'Library of Congress'],
	['worldcat',   'worldcat',   'WorldCat'],
	['isbndb',     'isbndb',     'ISBNdb'],
	# 'amazon', 'amazon'
]
ALL_SERVICES = [s[0] for s in SERVICE_LIST]
DEFAULT_SERVICE = ALL_SERVICES[0]

_DEV_MODE = True


### IMPLEMENTATION ###

def parse_args():
	# Construct the option parser.
	usage = '%prog [options] FILES ...'
	version = "version %s" %  __version__	
	epilog='Each ISBN must be 10 or 13 character ISBNs. ' \
		'Hyphens are permitted, spaces are not. Case is insensitive.'
	optparser = OptionParser (usage=usage, version=version, epilog=epilog)
	
	optparser.add_option ('--query', '-q',
		dest="query_services",
		type='string',
		action='append',
		help='''Which webservices to query.''',
		metavar='SERVICE',
	)
			
	optparser.add_option ('--name', '-n',
		dest="name_fmt",
		help="The layout for the new name. By default it will be '%s'" % \
			DEFAULT_NAME_FMT,
		metavar='FORMAT',
		default=DEFAULT_NAME_FMT,
	)
	
	optparser.add_option ('--debug', '-d',
		dest="debug",
		action='store_true',
		help='''In the event of errors, a full traceback will be issued, not just the error message.''',
	)
			
	#optparser.add_option ('--verbose', '-v',
	#	 dest="verbose",
	#	 help='''How much output to generate.''')
			
	options, infiles = optparser.parse_args()
	if (not infiles):
		optparser.error ('No input files specified')
	
	return infiles, options


def main():
	out_fmt, infiles, options = parse_args()
	try:
		for in_path in infiles:
			# construct parameters
			dir_name, file_name = path.split (in_path) 
			base_name, orig_ext = path.splitext (file_name)

			in_fmt = (options.input_format or
				IN_EXT_MAP.get (orig_ext, '')).lower()
			assert (in_fmt), \
				"no input format specified and can't derive from filename"
			out_ext = options.output_extension or OUT_EXT_MAP[out_fmt]
			out_path = path.join (dir_name, '%s.%s' % (base_name, out_ext))
			# read
			in_hndl = open (in_path, 'rb')
			in_seqs = [x for x in SeqIO.parse (in_hndl, in_fmt)]
			in_hndl.close()
			assert (in_seqs), "No sequences read from '%s'. " \
				"Perhaps the file is not in '%s' format." % (file_name, in_fmt)
			# write
			out_hndl = open (out_path, 'wb')
			SeqIO.write (in_seqs, out_hndl, out_fmt)
			out_hndl.close()
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
