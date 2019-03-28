upload_sbol.py
########################################

upload_sbol.py is a Python script for uploading the contents of SBOL files to specified collections and sub-collections on SynBioHub. It defines a class called SynBioHub that includes methods for the following:

1. Uploading SBOL Documents to specified SynBioHub collections.

2. Querying members of SynBioHub collections.

3. Uploading lab parameters to experiment plans and samples in SynBioHub.

.. contents::

.. section-numbering::

Specification
=============

The arguments to upload_sbol.py are listed below. Optional arguments have their default values listed as well.

.. code-block:: powershell

	-e, --email         			[E-mail address for SynBioHub account]
	-p, --password     				[Password for SynBioHub account]
	-u, --url 						[URL for target SynBioHub, default is https://hub.sd2e.org]
	-s, --sparql           			[SPARQL endpoint for target SynBioHub, default is http://hub-api.sd2e.org:80/sparql]

	-f, --sbol_files				[File paths to SBOL files for upload, default is all .xml files in current directory]
	-c, --collection_uri			[URI for target root collection in SynBioHub that will contain uploaded objects]
	-w, --overwrite                 [Set to overwrite any conflicting non-sub-collection objects in target collection]
	-W, --overwrite_sub_collections [Set to overwrite any conflicting sub-collections in target collection, otherwise will merge conflicting sub-collections]
	-m, --max_upload                [Max objects uploaded in single submission, will split upload into multiple submissions if necessary]

	-i, --sub_collection_id         [ID for new sub-collection to hold all uploaded objects]
	-n, --sub_collection_name       [Name for new sub-collection]
	-d, --sub_collection_description[Description for new sub-collection]
	-v, --sub_collection_version   	[Version for new sub-collection, default is 1]

	-I, --collection_id             [ID for new root collection in SynBioHub to hold all uploaded objects]
	-N, --collection_name           [Name for new root collection in SynBioHub]
	-D, --collection_description    [Description for new root collection in SynBioHub]
	-V, --collection_version   		[Version for new root collection in SynBioHub, default is 1]

Examples
========

An example of running upload_sbol.py from the Command Prompt after changing your working directory to upload_sbol is shown below. This example assumes that you wish to upload a file to the design collection and yeast gates sub-collection of the SD2 SynBioHub instance and overwrite any existing entities with the same URI as those in your file without deleting any of their bead model and bead batch properties. Bracketed argument values should be replaced with your own.

.. code-block:: powershell

    python upload_sbol.py -i [path_to_SBOL_file.xml] -w -p [password for sd2_service@sd2e.org at https://hub.sd2e.org] -b 'https://hub.sd2e.org/user/sd2e/design/yeast_gates/1' -l http://sd2e.org#bead_model http://sd2e.org#bead_batch

Equivalently, you can import the SynBioHub class and use it as shown below assuming that you have created a Document called doc:

.. code-block:: python

	from synbiohub_adapter.upload_sbol import SynBioHub

    sbh = SynBioHub('https://hub.sd2e.org', 'sd2_service@sd2e.org', 'insert_password_here', 'http://hub-api.sd2e.org:80/sparql', {'http://sd2e.org#bead_model', 'http://sd2e.org#bead_batch'})
    sbh.submit_to_collection(doc, 'https://hub.sd2e.org/user/sd2e/design/design_collection/1', True, ['https://hub.sd2e.org/user/sd2e/design/yeast_gates/1'])

You can also upload a lab parameter for an experiment plan or sample in SynBioHub by performing method calls like the following:

.. code-block:: python

	sbh.push_lab_plan_parameter('insert_URI_for_experiment_plan_here', 'http://sd2e.org#positive_control', 'insert_valid_positive_control_URI_here')

    sbh.push_lab_sample_parameter('insert_URI_for_sample_here', 'http://sd2e.org#bead_model', 'insert_valid_bead_model_URI_here')

Finally, you can attach a file to any URI in SynBioHub by performing the following method call:

.. code-block:: python

	sbh.attach_file('path_to_file', 'uri')