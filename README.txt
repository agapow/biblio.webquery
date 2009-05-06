Introduction
============

This package presents a number of methods for querying webservices for
bibliographic information, and includes two scripts for querying and renaming
files by ISBN.


Installation
============

biblio.webquery [#homepage]_ can be installed in a number of ways.
setuptools [#setuptools]_ is preferred, but a manual installation will
suffice.

Via setuptools / easy_install
-----------------------------

From the commandline call::

	% easy_install biblio.webquery

Superuser privileges may be required. 


Via setup.py
------------

Download a source tarball, unpack it and call setup.py to
install::

	% tar zxvf biblio.webquery.tgz
	% cd biblio.webquery
	% python setup.py install

Superuser privileges may be required. 


Usage
=====

Depending on your platform, the scripts may be installed as ``.py`` scripts,
or some form of executable, or both.


queryisbn
---------

Return bibliographic information from webservices for supplied ISBNs.

::

	queryisbn.py [options] ISBNs ...


with the options:

--version             show program's version number and exit
-h, --help            show this help message and exit
--debug               For errors, issue a full traceback instead of just a
                      message.
-s SERVICE, --service=SERVICE
                      The webservice to query. Choices are xisbn (WorldCat
                      xISBN), isbndb (ISBNdb). The default is xisbn.
-k KEY, --key=KEY     The access key for the webservice, if one is required.


For example::

	% queryisbn.py 1568385048 1564145026
	1568385048:
	   title: Drop the rock : removing character defects
	   authors: [Bill Pittman, Todd Weber]
	   publisher: Hazelden
	   year: 1999
	   lang: eng
	1564145026:
	   title: Stop clutter from stealing your life : discover why you clutter and how you can stop
	   authors: [Mike Nelson]
	   publisher: New Page Books
	   year: 2001
	   lang: eng
	% /queryisbn.py --debug -s isbndb -k OPNH8HG2 1568385048 1564145026
	1568385048:
	   title: Drop the Rock: Removing Character Defects
	   authors: [Bill Pittman, Todd Weber]
	1564145026:
	   authors: [Mike Nelson]



renamebyisbn
------------

Extract an ISBN from a file name, look up the associated bibliographic
information in a webservice and rename the file appropriately.

::

	renamebyisbn.py [options] FILES ...

with the options:

--version             show program's version number and exit
-h, --help            show this help message and exit
--debug               For errors, issue a full traceback instead of just a
                      message.
-s SERVICE, --service=SERVICE
                      The webservice to query. Choices are xisbn (WorldCat
                      xISBN), isbndb (ISBNdb). The default is xisbn.
-k KEY, --key=KEY     The access key for the webservice, if one is required.
-c CASE, --case=CASE  Case conversion of the new file name. Choices are
                      orig, upper, lower.The default is orig.
--leave_whitespace    Leave excess whitespace. By default, consecutive
                      spaces in names are compacted
--replace_whitespace=REPLACE_WHITESPACE
                      Replace whitespace in the new name with this string.
--strip_chars=STRIP_CHARS
                      Remove these characters from the new name. By default
                      this are ':!,'".?()'.
--overwrite           Overwrite existing files.
--dryrun              Check function and without renaming files.
--template=TEMPLATE   The form to use for renaming the file. The fields
                      recognised are auth (primary authors family name),
                      title (full title of the book), short_title
                      (abbreviated title), isbn, year (year of publication).
                      The default is
                      '%(auth)s%(year)s_%(short_title)s_(isbn%(isbn)s)'.
--unknown=UNKNOWN     Use this string if value is undefined.

The new name is generated first before the various processing options are
applied. In order, characters are stripped from the name, excess whitespace is
collapsed and then the case conversion is applied. We suggest you try a dryrun
before renaming any files. The file extension, if any, is removed before renaming and re-applied afterwards.

For example, working with 4 files called '0763718165.Jones Course.djvu', 'helm_0671708821 (orig).pdf', 'tutor_9780198568322.rar', 'unce.9783540237730.27380.pdf'::

	% renamebyisbn.py --dryrun books/*
	Original books/0763718165.Jones Course.djvu ...
	~ extracted ISBN 0763718165 ...
	~ found Andersen - Data structures in Java : a laboratory course
	~ new name Andersen2001_Data structures in Java_isbn0763718165.
	~ new path books/Andersen2001_Data structures in Java_isbn0763718165.djvu.
	Original books/helm_0671708821 (orig).pdf ...
	~ extracted ISBN 0671708821 ...
	~ found Helmstetter - What to say when you talk about yourself.
	~ new name Helmstetter1990_What to say when you talk about yourself_isbn0671708821.
	~ new path books/Helmstetter1990_What to say when you talk about yourself_isbn0671708821.pdf.
	Original books/tutor_9780198568322.rar ...
	~ extracted ISBN 9780198568322 ...
	~ found Skilling - Data analysis : a Bayesian tutorial ; [for scientists and engineers]
	~ new name Skilling2006_Data analysis_isbn9780198568322.
	~ new path books/Skilling2006_Data analysis_isbn9780198568322.rar.
	Original books/unce.9783540237730.27380.pdf ...
	~ extracted ISBN 9783540237730 ...
	~ found McDaniel - Uncertainty and surprise in complex systems questions on working with the unexpected
	~ new name McDaniel2005_Uncertainty and surprise in complex systems questions on working with the unexpected_isbn9783540237730.
	~ new path books/McDaniel2005_Uncertainty and surprise in complex systems questions on working with the unexpected_isbn9783540237730.pdf.
	
	% renamebyisbn.py --case lower --replace_whitespace ' ' --template '%(auth)s%(year)s_%(short_title)s_isbn%(isbn)s' books/*
	Original books/0763718165.Jones Course.djvu ...
	~ extracted ISBN 0763718165 ...
	~ found Andersen - Data structures in Java : a laboratory course
	~ new name andersen2001_data-structures-in-java_isbn0763718165.
	~ new path books/andersen2001_data-structures-in-java_isbn0763718165.djvu.
	~ renaming file
	Original books/helm_0671708821 (orig).pdf ...
	~ extracted ISBN 0671708821 ...
	~ found Helmstetter - What to say when you talk about yourself.
	~ new name helmstetter1990_what-to-say-when-you-talk-about-yourself_isbn0671708821.
	~ new path books/helmstetter1990_what-to-say-when-you-talk-about-yourself_isbn0671708821.pdf.
	~ renaming file
	Original books/tutor_9780198568322.rar ...
	~ extracted ISBN 9780198568322 ...
	~ found Skilling - Data analysis : a Bayesian tutorial ; [for scientists and engineers]
	~ new name skilling2006_data-analysis_isbn9780198568322.
	~ new path books/skilling2006_data-analysis_isbn9780198568322.rar.
	~ renaming file
	Original books/unce.9783540237730.27380.pdf ...
	~ extracted ISBN 9783540237730 ...
	~ found McDaniel - Uncertainty and surprise in complex systems questions on working with the unexpected
	~ new name mcdaniel2005_uncertainty-and-surprise-in-complex-systems-questions-on-working-with-the-unexpected_isbn9783540237730.
	~ new path books/mcdaniel2005_uncertainty-and-surprise-in-complex-systems-questions-on-working-with-the-unexpected_isbn9783540237730.pdf.
	~ renaming file



Developer notes
===============

biblio.webquery presents several classes that may be useful to other developers::

	* BaseWebQuery, a simple class for encapsulating queries to webservices
	
	* BaseKeyedWebQuery, ditto except allowing for access keys
	
	* XisbnQuery and IsbndbQuery, for fetching bibliographic information from
	Worldcat xISBN and ISBNdb services respectively
	
	* QueryThrottle, for limiting the frequency or total number of service
	queries.
	
	* BibRecord, a general class for holding bibliographic information
	
	* PersonalName, a class for holding a name along functions for parsing
	names into this class.


Consult the API documentation and scripts for further information.

Thanos Vassilakis has posted what looks like `a very useful module
<http://pypi.python.org/pypi/book>`__ for querying by ISBN. However it seems
to have disappeared from its home website.

The ``biblio`` namespace is open to other developers.


References
==========

.. [#homepage] `biblio.webquery homepage <http://www.agapow/net/software/biblio.webquery>`__

.. [#setuptools] `Installing setuptools <http://peak.telecommunity.com/DevCenter/setuptools#installing-setuptools>`__



