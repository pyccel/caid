# -*- coding: UTF-8 -*-
#! /usr/bin/python
import sys
from numpy.distutils.core import setup
from numpy.distutils.core import Extension

NAME    = 'caid'
VERSION = '0.2'
AUTHOR  = 'Ahmed Ratnani'
EMAIL   = 'ratnaniahmed@gmail.com'
URL     = 'http://www.ratnani.org/caid/'
DESCR   = 'Computer Aided Isogeometric Design.'
KEYWORDS = ['CAD', 'FEM', 'IGA', 'OpenGL']
LICENSE = "LICENSE.txt"

setup_args = dict(
    name             = NAME,
    version          = VERSION,
    description      = DESCR,
    long_description = open('README.rst').read(),
    author           = AUTHOR,
    author_email     = EMAIL,
    license          = LICENSE,
    keywords         = KEYWORDS,
    url              = URL,
#    download_url     = URL+'/get/default.tar.gz',
)

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
    if 'setuptools' in sys.modules:
        setup_args['install_requires'] = ['numpy']
    setup(  packages = packages \
          , package_dir=package_dir \
          , ext_modules=ext_modules \
          , **setup_args)

if __name__ == "__main__":
    setup_package()
