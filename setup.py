# -*- coding: UTF-8 -*-
#! /usr/bin/python

import os
import sys
#from setuptools import setup, find_packages
from setuptools import find_packages
from numpy.distutils.core import setup
from numpy.distutils.core import Extension
#import caid

NAME    = 'caid'
#VERSION = caid.__version__
VERSION = '0.2'
AUTHOR  = 'Ahmed Ratnani'
EMAIL   = 'ratnaniahmed@gmail.com'
URL     = 'http://www.ratnani.org/caid/'
DESCR   = 'Computer Aided Isogeometric Design.'
KEYWORDS = ['CAD', 'FEM', 'IGA', 'OpenGL']
LICENSE = "LICENSE.txt"

setup_args = dict(
    name                 = NAME,
    version              = VERSION,
    description          = DESCR,
    long_description     = open('README.rst').read(),
    author               = AUTHOR,
    author_email         = EMAIL,
    license              = LICENSE,
    keywords             = KEYWORDS,
    url                  = URL,
)

# ... we can't put igakit here, it's not working
install_requires = ['numpy', 'scipy']
# ...

packages=[  'caid' \
          , 'caid.quadrangles' \
          , 'caid.graphics' \
          , 'caid.numbering' \
          , 'caid.utils' \
          , 'caid.conversion' \
          , 'caid.core' \
         ]
package_dir={  'caid': 'caid'\
              ,'caid.quadrangles': 'caid/quadrangles' \
              ,'caid.graphics': 'caid/graphics' \
              ,'caid.numbering':  'caid/numbering' \
              ,'caid.utils':  'caid/utils' \
              ,'caid.conversion':  'caid/conversion' \
              ,'caid.core':  'caid/core' \
              ,}

ext_modules  = [ \
                # ... bsplines extension
                 Extension('caid.core.bspline', \
                           sources = ['caid/core/bspline.pyf', \
                                      'caid/core/bspline.F90'], \
                           f2py_options = ['--quiet'], \
                           define_macros = [ \
                                            #('F2PY_REPORT_ATEXIT', 0),
                                            ('F2PY_REPORT_ON_ARRAY_COPY', 0)] \
                          ), \
                # ...
                # ... hermite-bezier extension
                 Extension('caid.core.hbezier', \
                           sources = ['caid/core/hbezier.pyf', \
                                      'caid/core/hbezier.F90'], \
                           f2py_options = ['--quiet'], \
                           define_macros = [ \
                                            #('F2PY_REPORT_ATEXIT', 0),
                                            ('F2PY_REPORT_ON_ARRAY_COPY', 0)] \
                          ) \
                # ...
                ,]


def setup_package():
    try:
        import igakit
    except:
        print('could not find igakit. It will be installed.')

        cmd = 'install https://bitbucket.org/dalcinl/igakit/get/default.tar.gz'
        import sys
        if sys.version.split('.')[0] == '2':
            # using python2
            cmd = 'pip {0}'.format(cmd)
        elif sys.version.split('.')[0] == '3':
            # using python3
            cmd = 'pip3 {0}'.format(cmd)
        else:
            raise ValueError('Could not find python version.')

        # ...
        import argparse
        class MyParser(argparse.ArgumentParser):
            """
            Custom argument parser for printing help message in case of an error.
            See http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
            """
            def error(self, message):
                sys.stderr.write('error: %s\n' % message)
                self.print_help()
                sys.exit(2)
        # ...

        # ...
        parser = MyParser(description='CLAPP config command line')
        # ...

        # ...
        parser.add_argument('options', metavar='N', type=str, nargs='+')
        parser.add_argument('--prefix')
        # ...

        # ...
        try:
            args = parser.parse_args()
            prefix = args.prefix

            cmd = '{0} --prefix={1}'.format(cmd, prefix)
            os.system(cmd)
        except:
            cmd = 'sudo {0}'.format(cmd)
            os.system(cmd)
        # ...

    setup(packages=packages, \
          include_package_data=True, \
          package_dir=package_dir, \
          install_requires=install_requires, \
          ext_modules=ext_modules, \
          zip_safe=True, \
          **setup_args)

if __name__ == "__main__":
    setup_package()
