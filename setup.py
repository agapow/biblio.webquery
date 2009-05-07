from setuptools import setup, find_packages
import os
from glob import glob

from biblio.webquery import __version__

setup (
	name='biblio.webquery',
	version=__version__,
	description="Extracting bibliographic information from web services",
	long_description=open("README.txt").read() + "\n" +
		open(os.path.join("docs", "HISTORY.txt")).read(),
	classifiers=[
		"Programming Language :: Python",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
	keywords='web-service REST book',
	author='Paul-Michael Agapow',
	author_email='agapow@bbsrc.ac.uk',
	url='http://www.agapow.net/software/biblio.webquery',
	license='BSD',
	packages=find_packages(),
  
	namespace_packages=['biblio'],
	test_suite = 'nose.collector',
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'setuptools',
		# -*- Extra requirements: -*-
	],
	entry_points={
		'console_scripts': [
			'queryisbn = biblio.webquery.scripts.queryisbn:main',
			'renamebyisbn = biblio.webquery.scripts.renamebyisbn:main',
		],
	},
)
