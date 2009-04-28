#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Retreive bibliographic information for a given ISBN.

"""

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

_DEV_MODE = True


### IMPLEMENTATION ###

def parse_args():
	# Construct the option parser.
	usage = '%prog [options] ISBNs ...'
	version = "version %s" %  __version__	
	epilog='Each ISBN must be 10 or 13 character ISBNs. ' \
		'Hyphens are permitted, spaces are not. Case is insensitive.'
	optparser = OptionParser (usage=usage, version=version, epilog=epilog)
	
	optparser.add_option ('--input-format', '-i',
		dest="input_format",
		help='''The format of the input biosequence files. If not supplied, this will be inferred from the extension of the files.''',
		metavar='FORMAT',
	)
			
	optparser.add_option ('--output-extension', '-e',
		dest="output_extension",
		help='''The extension of the output biosequence files. If not supplied, this will be inferred from the output format.''',
		metavar='EXTENSION',
	)
	
	optparser.add_option ('--debug', '-d',
		dest="debug",
		action='store_true',
		help='''In the event of errors, a full traceback will be issued, not just the error message.''',
	)
			
	#optparser.add_option ('--verbose', '-v',
	#	 dest="verbose",
	#	 help='''How much output to generate.''')
			
	options, pargs = optparser.parse_args()
	
	if (len (pargs) < 1):
		optparser.error ('No output format specified')
	out_fmt = pargs[0].lower()
	if (out_fmt not in KNOWN_FMTS):
		optparser.error ("unknown output format '%s'" % out_fmt)
	infiles = pargs[1:]
	if (not infiles):
		optparser.error ('No input files specified')
	
	return out_fmt, infiles, options


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
