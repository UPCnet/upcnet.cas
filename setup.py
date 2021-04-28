from setuptools import setup, find_packages
import os

version = '1.7'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='upcnet.cas',
      version=version,
      description="",
      long_description=README + "\n" + HISTORY,
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
