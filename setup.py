#############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.security package
"""
import os
import platform
import sys
from setuptools import Extension
from setuptools import find_packages
from setuptools import setup

TESTS_REQUIRE = [
    'zope.component',
    'zope.configuration',
    'zope.location',
    'zope.testing',
    'zope.testrunner',
]

def alltests():
    import os
    import sys
    import unittest
    # use the zope.testrunner machinery to find all the
    # test suites we've put under ourselves
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    args = sys.argv[:]
    defaults = ["--test-path", here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)

here = os.path.abspath(os.path.dirname(__file__))
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

# Include directories for C extensions
# Sniff the location of the headers in 'persistent' or fall back
# to local headers in the include sub-directory

class ModuleHeaderDir(object):

    def __init__(self, require_spec, where='../..'):
        # By default, assume top-level pkg has the same name as the dist.
        # Also assume that headers are located in the package dir, and
        # are meant to be included as follows:
        #    #include "module/header_name.h"
        self._require_spec = require_spec
        self._where = where

    def __str__(self):
        from pkg_resources import require
        from pkg_resources import resource_filename
        from pkg_resources import DistributionNotFound
        try:
            require(self._require_spec)
            path = resource_filename(self._require_spec, self._where)
        except DistributionNotFound:
            path = os.path.join(here, 'include')
        return os.path.abspath(path)

include = [ModuleHeaderDir('zope.proxy')]

# Jython cannot build the C optimizations, while on PyPy they are
# anti-optimizations (the C extension compatibility layer is known-slow,
# and defeats JIT opportunities).
py3 = sys.version_info[0] >= 3
py_impl = getattr(platform, 'python_implementation', lambda: None)
pure_python = os.environ.get('PURE_PYTHON', False)
is_pypy = py_impl() == 'PyPy'
is_jython = 'java' in sys.platform

if pure_python or is_pypy or is_jython:
    setup_requires = []
    ext_modules = []
else:
    setup_requires = ['zope.proxy >= 4.1.0']
    ext_modules = [
        Extension("zope.security._proxy",
                  [os.path.join('src', 'zope', 'security', "_proxy.c")],
                  include_dirs=include,
                 ),
        Extension("zope.security._zope_security_checker",
                  [os.path.join('src', 'zope', 'security',
                                        "_zope_security_checker.c")]
                 ),
    ]

setup(name='zope.security',
      version='4.0.4.dev0',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope Security Framework',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
          ),
      keywords = "zope security policy principal permission",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.security',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      setup_requires=setup_requires,
      ext_modules=ext_modules,
      install_requires=['setuptools',
                        'zope.component',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.location',
                        'zope.proxy >= 4.1.0',
                        'zope.schema',
                        ],
      test_suite = '__main__.alltests',
      tests_require=TESTS_REQUIRE,
      extras_require = dict(
          pytz=["pytz"],
          untrustedpython=['zope.untrustedpython'] if not py3 else [],
          zcml=['zope.configuration'],
          test=TESTS_REQUIRE,
          testing=TESTS_REQUIRE + ['nose', 'coverage'],
          docs=['Sphinx', 'repoze.sphinx.autointerface'],
          ),
      include_package_data = True,
      zip_safe = False,
      )
