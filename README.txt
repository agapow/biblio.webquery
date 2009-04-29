Introduction
============

This package presents a number of methods for querying webservices for
bibliographic information, primarily via the ISBN.


Installation
============

bioscripts.convert [#homepage]_ can be installed in a number of ways.
Biopython [#biopython]_ is required. Either of the automated methods using
setuptools [#setuptools]_ are preferred, but a manual installation will
suffice if need be.

Via setuptools / easy_install
-----------------------------

From the commandline call::

	% easy_install bioscripts.convert

Superuser privileges may be required. 


Via setup.py
------------

Download a source tarball, unpack it and call setup.py to
install::

	% tar zxvf bioscripts.convert.tgz
	% cd bioscripts.convert
	% python setup.py install

Superuser privileges may be required. 


Usage
=====

Due to limitations on identifiers in certain formats, sequence names may
differ between input and output files. For certain alignment formats, all
incoming sequences must be of the same length, as required by the output
format. Not all formats understood by Biopython have been enabled, due to
being untested or incomplete. Certain output formats (e.g. Nexus, Genbank)
require explicit information about alphabet (sequence type), that is not
provided by certain input formats (e.g. Fasta).

In certain error conditions, an empty output file will be created.

Depending on your platform, the scripts may be installed as ``.py`` scripts,
or some form of executable, or both.


convbioseq
----------

::

	convbioseq.py [options] FORMAT INFILES ...

with the options:

--version       show program's version number and exit
-h, --help      show this help message and exit
-i FORMAT, --input-format=FORMAT
                The format of the input biosequence files. If not
                supplied, this will be inferred from the extension of
                the files.
-e EXTENSION, --output-extension=EXTENSION
                The extension of the output biosequence files. If not
                supplied, this will be inferred from the output
                format.
-d, --debug     In the event of errors, a full traceback will be
                issued, not just the error message.

FORMAT must be one of 'clustal', 'fasta', 'genbank', 'nexus', 'phd', 'phylip',
'qual', 'stockholm'. The input formats inferred from extensions are clustal
('.aln'), genbank ('.genbank'), nexus ('.nxs'), nexus ('.nexus'), phylip
('.phylip'), stockholm ('.sth'), phd ('.phd'), qual ('.qual'), phylip
('.phy'), clustal ('.clustal'), genbank ('.gb'), tab ('.tab'), fasta
('.fasta'), stockholm ('.stockholm'). The default extensions for output
formats are '.aln' (clustal), '.nexus' (nexus), '.phy' (phylip), '.phd' (phd),
'.qual' (qual), '.gb' (genbank), '.sth' (stockholm), '.fasta' (fasta).

For example::

	% convbioseq.py clustal one.fasta two.nxs three.stockholm

will produce three clustal formatted files 'one.aln', 'two.aln' and
'three.aln' from files it assumes are Fasta, Nexus and Stockholm formatted
respectively.

	% convbioseq.py -i phylip clustal one.fasta two.nxs

will produce two Phylip formatted files 'one.phy' and 'two.phy' and from files
it assumes are Fasta formatted.

	% convbioseq.py -e foo clustal one.fasta two.nxs

will produce two Clustal formatted files 'one.foo' and 'two.foo' from files
it assumes are Fasta and Nexus formatted respectively.	


convalign
---------

::

	convalign.py [options] FORMAT INFILES ...

with the options:

  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i FORMAT, --input-format=FORMAT
                        The format of the input alignment files. If not
                        supplied, this will be inferred from the extension of
                        the files.
  -e EXTENSION, --output-extension=EXTENSION
                        The extension of the output alignment files. If not
                        supplied, this will be inferred from the output
                        format.

FORMAT must be one of 'clustal', 'fasta', 'nexus', 'phylip', 'stockholm'. The
input formats inferred from extensions are clustal ('.aln'), nexus ('.nxs'),
nexus ('.nexus'), phylip ('.phylip'), stockholm ('.sth'), phylip ('.phy'),
clustal ('.clustal'), stockholm ('.stockholm'), fasta ('.fasta'). The default
extensions for output formats are '.nxs' (nexus), '.phy' (phylip), '.fasta'
(fasta), '.aln' (clustal), '.sth' (stockholm).


Developer notes
===============

This module is not intended for importing, but the setuptools packaging and
infrastructure make for simple distribution of scripts, allowing the checking
of prerequisites, consistent installation and updating.

The ``bioscripts`` namespace was chosen as a convenient place to "keep" these
scripts and is open to other developers.


References
==========

.. [#homepage] `bioscripts.convert homepage <http://www.agapow/net/software/bioscripts.convert>`__

.. [#setuptools] `Installing setuptools <http://peak.telecommunity.com/DevCenter/setuptools#installing-setuptools>`__

* Thanos Vassilakis has posted what looks like `a very useful module
  <http://pypi.python.org/pypi/book>`__ for querying by ISBN. However it seems
  to have disappeared from its home website.


