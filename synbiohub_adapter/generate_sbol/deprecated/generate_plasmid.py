from sbol import *
import os

# This example script generates SBOL for a plasmid

# Configure the working document

doc = Document()

setHomespace('http://hub.sd2e.org/user/sd2e/design')
Config.setOption('sbol_typed_uris', False)

# Create a ComponentDefinition for the plasmid and give
# it the type URIs for 'DNA' and 'circular'

plasmid = ComponentDefinition('plasmid_id_2', BIOPAX_DNA, '1')
plasmid.name = 'Plasmid 2'
plasmid.description = 'This is a plasmid.'
plasmid.types = plasmid.types + ['http://identifiers.org/so/SO:0000988']

# Add plasmid to the working document

doc.addComponentDefinition(plasmid)

# Write the working document out to an SBOL file

doc.write(os.path.join(os.getcwd(), 'plasmid2.xml'))