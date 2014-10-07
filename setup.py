# -*- coding: UTF-8 -*-
#! /usr/bin/python

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
    long_description = open('README.md').read(),
    author           = AUTHOR,
    author_email     = EMAIL,
    license          = LICENSE,
    keywords         = KEYWORDS,
    url              = URL,
#    download_url     = URL+'/get/default.tar.gz',
)

packages=[  'caid' \
          , 'caid.graphics' \
          , 'caid.utils' \
         ]
package_dir={  'caid': 'src/caid'\
              ,'caid.graphics': 'src/caid/graphics' \
              ,'caid.utils':  'src/caid/utils' \
              ,}

def setup_package():
    import sys
    from numpy.distutils.core import setup
    from numpy.distutils.core import Extension
    if 'setuptools' in sys.modules:
        setup_args['install_requires'] = ['numpy']
    setup(  packages = packages \
          , package_dir=package_dir
          , **setup_args)

if __name__ == "__main__":
    setup_package()
