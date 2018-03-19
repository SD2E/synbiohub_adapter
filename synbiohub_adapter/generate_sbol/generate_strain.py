from sbol import *
import os

# This example script generates SBOL for a host strain

# Configure the working document

doc = Document()

setHomespace('http://hub.sd2e.org/user/sd2e/design')
Config.setOption('sbol_typed_uris', False)

# Create a ComponentDefinition for the strain and give
# it the type URI for 'organism strain'

strain = ComponentDefinition('strain_id', 'http://purl.obolibrary.org/obo/NCIT_C14419', '1')
strain.name = 'Strain'
strain.description = 'This is the wild type strain.'

# Add strain to the working document

doc.addComponentDefinition(strain)

# Write the working document out to an SBOL file

doc.write(os.path.join(os.getcwd(), 'strain.xml'))