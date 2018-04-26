generate_sbol
########################################

generate_sbol is a Python script for converting CSV-formatted genetic design data to the Synthetic Biology Open Language (SBOL).

.. contents::

.. section-numbering::


Installation
============

generate_sbol requires the pySBOLx module, which you can install by running the following command from the synbiohub_adapter repo:

.. code-block:: powershell

    python setup.py install

Usage
=====

generate_sbol can be run from its directory as follows:

.. code-block:: powershell

    python generate_sbol.py -i [paths to input CSV files] -o [path to output SBOL RDF/XML file] -om [path to OM RDF file (unit reference)]

If -i is not included, then all CSV files in the current directory will be converted. If -o is not included, then an output SBOL file named generated_sbol.xml will be added to the current directory. If -om is not included, then generate_sbol will look for a file named om-2.0.rdf in the current directory. If this file is not found, then no units from the input CSV files will be converted to SBOL.

Example
--------

Run the following command from the generate_sbol directory:

.. code-block:: powershell

    python generate_sbol.py -i yeast_gates\YG_composite.csv