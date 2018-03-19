from sbol import *
import os

# This example script generates SBOL for a logic gate

# Configure the working document

doc = Document()

setHomespace('http://hub.sd2e.org/user/sd2e/design')
Config.setOption('sbol_typed_uris', False)

# Load SBOL files for a strain and two plasmids
# into the working document

doc.append(os.path.join(os.getcwd(), 'strain.xml'))
doc.append(os.path.join(os.getcwd(), 'plasmid1.xml'))
doc.append(os.path.join(os.getcwd(), 'plasmid2.xml'))

# Create a ModuleDefinition for the logic gate
# and give it the role URI for 'logic operator'

gate = ModuleDefinition('gate_id_1', '1')
gate.name = 'Gate 1'
gate.description = 'This is a gate.'
gate.roles = ['http://edamontology.org/data_2133']

# Create a FunctionalComponent reference in the gate 
# ModuleDefinition to each strain/plasmid ComponentDefinition

for comp in doc.componentDefinitions:
	fc = gate.functionalComponents.create(comp.displayId)
	fc.definition = comp.identity

# Add gate to the working document

doc.addModuleDefinition(gate)

# Write the working document out to an SBOL file

doc.write(os.path.join(os.getcwd(), 'gate1.xml'))