CAID is a multi-platform software that has been designed for IsoGeometric Analysis Pre and Post Processing. Its design goal is to provide a fast, light and user-friendly designer and meshing tool.

The Post-Processing and advanced visualization capabilities are still under development, as well as an optimized 3D computing engine.

For more details, please read [**CAID**](http://ratnani.org/caid_doc/)

Requierements
=============

**numpy**
---------

[**NumPy**](http://www.numpy.org/) is the fundamental package for scientific computing with Python

Installation can be done using

   `sudo apt-get install python-numpy`

**scipy**
---------

[**SciPy**](http://www.scipy.org/) is a Python-based ecosystem of open-source software for mathematics, science, and engineering.

Installation can be done using

   `sudo apt-get install python-scipy`

You can install both **numpy** and **scipy** using 

    `sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose`

**igakit**
----------

[**igakit**](http://bitbucket.org/dalcinl/igakit) is a package that implements many of the NURBS routines from Piegl's book using Fortran and Python.

**wxPython**
------------

Install *wxGTK 2.8* with the command

   `sudo apt-get install python-wxgtk2.8`

Verify that everything is OK

    import wx
    import wxversion

**PyOpenGL**
------------

[**PyOpenGL**](http://pyopengl.sourceforge.net/) is the most common cross platform Python binding to OpenGL and related APIs.

Installation can be done using [**pip**](https://pypi.python.org/pypi/pip)

   `sudo pip install PyOpenGL PyOpenGL_accelerate`

CAID
====

**CAID** is a full *Python* software. No need for a specific installation, once you have filled the previous requierements. If you want to run **CAID** as the following

Usage
-----

    caid session.wkl

In this case, please add the following lines in your *.bashrc/.bash_profile*

    # CAID 
    export CAID_DIR=/home/ratnani/Projects/pigasus/trunk/caid
    alias caid="python $CAID_DIR/src/caid.py"
    #
