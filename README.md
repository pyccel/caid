CAID is a multi-platform software that has been designed for IsoGeometric Analysis Pre and Post Processing. Its design goal is to provide a fast, light and user-friendly designer and meshing tool.

The Post-Processing and advanced visualization capabilities are still under development, as well as an optimized 3D computing engine.

For more details, please read **CAID** "http://ratnani.org/caid_doc/"

Requierements
=============

* **wxPython**

Install *wxGTK 2.8* with the command::

   sudo apt-get install python-wxgtk2.8

Verify that everything is OK

.. code-block:: python

   import wx
   import wxversion

* **PyOpenGL**

* **scipy**

* **numpy**

* **igakit**


CAID
====

**CAID** is a full *Python* software. No need for a specific installation, once you have filled the previous requierements. If you want to run **CAID** as the following::

   caid session.wkl

In this case, please add the following lines in your *.bashrc/.bash_profile*::

   # CAID 
   export CAID_DIR=/home/ratnani/Projects/pigasus/trunk/caid
   alias caid="python $CAID_DIR/src/caid.py"
   #
