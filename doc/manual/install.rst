.. role:: envvar(literal)
.. role:: command(literal)
.. role:: file(literal)
.. _INSTALL:

Install
=======

In this section, we present all you need to install and run CAID. As mentioned before, CAID is based on `igakit <http://bitbucket.org/dalcinl/igakit>`_ a package that implements many of the NURBS routines from Piegl's book using Fortran and Python. However, the included  version of *igakit* was modified to take into account multi-patch description and gradiant maps.

Requierements
*************

* **wxPython**

* **PyOpenGL**

* **scipy**

* **numpy**

.. note:: You can install **canopy** in order to get all these packages, which I preconise. However, I prefer to install them by hand.  

IgaKit
-----

The required version of *igakit* is given with the **Pigasus** suite distribution. Please look at the corresponding *README* file for more information.

CAID
------

**CAID** is a full *Python* software. No need for a specific installation, once you have filled the previous requierements. If you want to run **CAID** as the following::

   caid session.wkl

In this case, please add the following lines in your *.bashrc/.bash_profile*::

   # CAID 
   export CAID_DIR=/home/ratnani/Projects/pigasus/trunk/caid
   alias caid="python $CAID_DIR/src/caid.py"
   #

Installation of *wxpython*
^^^^^^^^^^^^^^^^^^^^^^^^^^

Install wxGTK 2.8 with the command::

  sudo apt-get install python-wxgtk2.8

Verify that everything is OK

.. code-block:: python

   import wx
   import wxversion

.. Local Variables:
.. mode: rst
.. End:
