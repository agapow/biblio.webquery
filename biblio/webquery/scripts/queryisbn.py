#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Retreive bibliographic information for a given ISBN.

"""
# TODO: throttle parameter?
# TODO: Amazon query?
# TODO: output in other formats?

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import sys
from os import path
from optparse import OptionParser
from exceptions import BaseException

from Bio import SeqIO

try:
	from biblio.webquery import __version__
except:
	__version__ = 'unknown'
	

### CONSTANTS & DEFINES ###

WEBSERVICES = [
	{
		'id':      'xisbn', 
		'title':   'WorldCat xISBN',
		'ctor':    'XisbnQuery',
	},
	{
		'id':      'isbndb', 
		'title':   'ISBNdb',
		'ctor':    'IsbndbQuery',
	},
	{
		'id':      'loc', 
		'title':   'Library of Congress',
		'ctor':    'LocQuery',
	},
]
DEFAULT_WEBSERVICE = WEBSERVICES[0]
WEBSERVICE_LOOKUP = dict ([(s['id'], s) for s in WEBSERVICES])

_DEV_MODE = True


### IMPLEMENTATION ###

def parse_args():
	# Construct the option parser.
	usage = '%prog [options] ISBNs ...'
	version = "version %s" %  __version__	
	epilog='',
	optparser = OptionParser (usage=usage, version=version, epilog=epilog)
	
	optparser.add_option ('--service', '-s',
		dest='webservice',
		help="The webservice to query. By default it is '%s' (%s)." % (
			DEFAULT_WEBSERVICE['title'], DEFAULT_WEBSERVICE['id']) ,
		metavar='WEBSERVICE',
		default=DEFAULT_WEBSERVICE['id'],
	)
	
	optparser.add_option ('--key', '-k',
		dest="service_key",
		help='''The access key for the webservice, if one is required.''',
		metavar='KEY',
		default=None,
	)	
	
	optparser.add_option ('--debug', '-d',
		dest="debug",
		action='store_true',
		help='For errors, issue a full traceback instead of just a message.',
	)
			
			
	options, isbns = optparser.parse_args()
	
	if (not isbns):
		optparser.error ('No ISBNs specified')
	serv = WEBSERVICE_LOOKUP.get (options.webservice, None)
	if (not serv):
		optparser.error ("Unrecognised webservice '%s'" % options.webservice)
	if (isinstance (serv, BaseKeyedWebQuery)):
		if (not options.service_key):
			optparser.error ("%s webservice requires access key" % serv['title'])
	else:
		if (options.service_key):
			optparser.error ("%s webservice does not require access key" %
				serv['title'])
	
	return isbns, options


def main():
	out_fmt, infiles, options = parse_args()
	try:
		for in_path in infiles:
			# construct parameters
			dir_name, file_name = path.split (in_path) 
			base_name, orig_ext = path.splitext (file_name)
			if (orig_ext.startswith ('.')):
				orig_ext = orig_ext[1:]
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
