from setuptools import setup, find_packages
import os

version = '1.4'

setup(name='upcnet.cas',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='cas plone zope upcnet genweb',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/UPCnet/upcnet.cas.git',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upcnet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'anz.casclient'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
