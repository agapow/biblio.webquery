from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='biblio.webquery',
      version=version,
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
      url='http://www.agapow.net/software/bibliowebquery',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['biblio'],
		test_suite = 'nose.collector',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
