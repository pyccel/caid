CAID is a multi-platform software that has been designed for IsoGeometric Analysis Pre and Post Processing. Its design goal is to provide a fast, light and user-friendly designer and meshing tool.

The Post-Processing and advanced visualization capabilities are still under development, as well as an optimized 3D computing engine.

For more details, please read [**CAID**](http://ratnani.org/caid_doc/)

**CAID** can be used in 2 different ways:

* as a *python* package: using *ipython* or *scripts* 

* as a GUI modeler: for a better interactive use

Common requierements
====================

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

**matplotlib**
--------------

[**Matplotlib**](http://www.matplotlib.org/) is a python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms. matplotlib can be used in python scripts, the python and ipython shell (ala MATLAB or Mathematica)

Installation can be done using

   `sudo apt-get install python-matplotlib`

**igakit**
----------

[**igakit**](http://bitbucket.org/dalcinl/igakit) is a package that implements many of the NURBS routines from Piegl's book using Fortran and Python.

GUI Requierements
=================

**wxPython**
------------

Install *wxGTK 2.8* with the command

   `sudo apt-get install python-wxgtk2.8`

Verify that everything is OK::

    import wx
    import wxversion

**PyOpenGL**
------------

[**PyOpenGL**](http://pyopengl.sourceforge.net/) is the most common cross platform Python binding to OpenGL and related APIs.

Installation can be done using [**pip**](https://pypi.python.org/pypi/pip)

   `sudo pip install PyOpenGL PyOpenGL_accelerate`

Installation
============

Installation can be done by runing the following command, giving **PATH_FOR_INSTALLATION**

    python setup.py install --prefix=PATH_FOR_INSTALLATION 

Add the following lines in your *.bashrc/.bash_profile* by replacing **PATH_TO_CAID_SRC**

    `alias caid="python $PATH_TO_CAID_SRC/caid-gui/main.py"`

Package-Usage
=============

Start by import the **CAID** package::

  import caid

In order to check that the fortran code has been well installed, use::

  import caid.core
  import caid.core.bspline
  import caid.core.hbezier

If you don't get any message, then everything seems to be fine.

Let's now import a *square* geometry and refine it::

  from caid.cad_geometry import square
  geo = square(n=[3,3], p=[2,2])
  geo.plotMesh()
  import matplotlib.pyplot as plt
  plt.show()

GUI-Usage
=========

Runing **CAID** can be done in different ways.

* without any argument

   `caid`

* with a given *workgroup* session

   `caid session.wkl`

* with given domains files session

   `caid domain1.xml domain2.xml domain3.xml`

* with a given field file

   `caid U.pfl`
