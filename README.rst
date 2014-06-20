======================================================
fancyTools - various fancy tools for every day usage
======================================================

- Browse the `API Documentation <http://radjkarl.github.io/fancyTools>`_
- Fork the code on `github <https://github.com/radjkarl/fancytools>`_


Installation
^^^^^^^^^^^^

**fancytools** is listed in the Python Package Index. You can install it typing::

    pip install fancytools

Tests
^^^^^^
**fancyTools** uses mostly the 'one class/function per file' rule. Running each module as program, like::

    python -m fancytools.pystructure.stichmodules

will execute the test procedure of this module.

To run all tests type::

    python -m fancytools.tests


Import Classes/Functions
^^^^^^^^^^^^^^^^^^^^^^^^
 
**fancytools** uses `autoXinit <https://pypi.python.org/pypi/autoxinit>`_ to automatically import all classes and modules in a package. Therefore you can import the function *stitchModules* via::

    from fancytools.pystructure import stitchModules

