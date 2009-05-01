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

import sys
from os import path, rename
from optparse import OptionParser
from exceptions import BaseException

from config import *
from common import *


### CONSTANTS & DEFINES ###

ISBN_PATS = [
	
]

ISBN_RE = [re.compile (p, re.IGNORECASE) for p in ISBN_PATS]

_DEV_MODE = True


### IMPLEMENTATION ###

def parse_args():
	# Construct the option parser.
	usage = '%prog [options] FILES ...'
	version = "version %s" %  script_version
	epilog='',path.split (fpath)
	optparser = OptionParser (usage=usage, version=version, epilog=epilog)
	add_shared_options (optparser)

	# parse and check args
	options, fpaths = optparser.parse_args()
	
	if (not fpaths):
		optparser.error ('No files specified')
	check_shared_options (optparser)
	
	## Postconditions & return:
	return fpaths, options


def base_ext_from_path (fpath):
	"""
	Return a files base name and extension from it's path.
	"""
	fdir, fname = path.split (fpath)
	return path.splitext (fname)


def rename_file (oldpath, newname):
	"""
	Rename a file, while keeping it in the same location.
	"""
	fdir, fname = path.split (fpath)
	newpath = path.join (fdir, newname)
	rename (oldpath, newpath)


def extract_isbn_from_filename (fname):


def main():
	fpath_list, options = parse_args()
	try:
		webqry = construct_webquery (options.webservice, options.service_key)
		for fpath in fpath_list:
			print '%s:' % fpath
			base, ext = base_ext_from_path (fpath)
			print '%s %s' % (base, ext)
			isbn = extract_isbn_from_filename (base)
			
			rec_list = webqry.query_bibdata_by_isbn (isbn, fmt='bibrecord')
			if (rec_list):
				for f in PRINT_FIELDS:
					if (getattr (rec_list[0], f)):
						print '   %s: %s' % (f, getattr (rec_list[0], f))
			else:
				print '   No results'
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
