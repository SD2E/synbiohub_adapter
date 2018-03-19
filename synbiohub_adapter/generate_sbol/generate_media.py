import rdflib
import csv
from sbol import *
import os

# Classes and methods for generating Ontology of units of Measure (OM) measures and units (i.e. for media ingredient concentrations)

OM_NS = 'http://www.ontology-of-units-of-measure.org/resource/om-2#'

class Measure(Identified, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, has_numerical_value=None, has_unit=None, version='1'):
        Identified.__init__(self, OM_NS + 'Measure', display_id, version)
        if name is not None:
            self.name = name
        if has_numerical_value is not None:
            self.hasNumericalValue = FloatProperty(self.this, OM_NS + 'hasNumericalValue', '0', '1', has_numerical_value)
        if has_unit is not None:
            self.hasUnit = URIProperty(self.this, OM_NS + 'hasUnit', '0', '1', has_unit)
        self.register_extension_class(Measure, 'om')
        
class Unit(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, symbol=None, version='1'):
        TopLevel.__init__(self, OM_NS + 'Unit', display_id, version)
        if name is not None:
            self.name = name
        if symbol is not None:
            self.symbol = TextProperty(self.this, OM_NS + 'symbol', '0', '1', symbol)
        self.register_extension_class(Unit, 'om')

def create_measure(mag, identified, unit=None, display_id=None, name=None, version='1'):
    if not hasattr(identified, 'measures'):
        identified.measures = OwnedPythonObject(identified.this, OM_NS + 'measure', Measure, '0', '*')

    if display_id is not None:
        ms_id = display_id
    else:
        ms_id = identified.displayId + '_measure'

    if name is not None:
        ms_name = name
    else:
        ms_name = ms_id

    try:
        ms = identified.measures.create(ms_id)
        ms.name = ms_name
        ms.version = version

        ms.hasNumericalValue = FloatProperty(ms.this, OM_NS + 'hasNumericalValue', '0', '1', mag)
        if unit is not None:
            ms.hasUnit = URIProperty(ms.this, OM_NS + 'hasUnit', '0', '1', unit.identity)
    except:
        ms = identified.measures.get(''.join([identified.persistentIdentity.get(), '/', ms_id, '/', version]))

def create_unit(doc, om, symbol=None, display_id=None, name=None, descr=None, version='1'):
    try:
        uri = ''.join(['<', OM_NS[:-1], '/', display_id, '>'])
        result = next(iter(om.query(''.join(["SELECT ?symbol ?name ?descr WHERE { ", uri, " om:symbol ?symbol ; rdfs:label ?name . OPTIONAL { ", uri, " rdfs:comment ?descr . FILTER (lang(?descr) = 'en') . } FILTER (lang(?name) = 'en') }"]))))
    except:
        try:
            result = next(iter(om.query(''.join(["SELECT ?uri ?name ?descr WHERE { ?uri om:symbol '", symbol, "' ; rdfs:label ?name . OPTIONAL { ?uri rdfs:comment ?descr . FILTER (lang(?descr) = 'en') . } FILTER (lang(?name) = 'en') }"]))))
        except:
            result = next(iter(om.query(''.join(["SELECT ?uri ?symbol ?descr WHERE { ?uri om:symbol ?symbol . {?uri rdfs:label '", name, "'@en . } UNION {?uri rdfs:label '", name, "'@nl } }"]))))

    try:
        unit_id = result.uri.split('/')[-1]
    except:
        unit_id = display_id


    unit = doc.getTopLevel(''.join([getHomespace(), '/', unit_id, '/', version]))

    if unit is not None:
        unit = unit.cast(Unit)
    else:
        try:
            unit_name = result.name
        except:
            if name is not None:
                unit_name = name
            else:
                unit_name = unit_id

        try:
            unit = Unit(unit_id, unit_name, result.symbol, version)
        except:
            if symbol is not None:
                unit = Unit(unit_id, unit_name, symbol, version)
            else:
                unit = Unit(display_id=unit_id, name=unit_name, version=version)
        try:
            unit.description = result.descr
        except:
            if descr is not None:
                unit.description = descr

        try:
            unit.wasDerivedFrom = unit.wasDerivedFrom + [result.uri]
        except:
            pass

        doc.addExtensionObject(unit)

    return unit

# Configure the OM resource and working document

om = rdflib.Graph()
om.parse('om-2.0.rdf')

doc = Document()

setHomespace('http://hub.sd2e.org/user/sd2e/design')
Config.setOption('sbol_typed_uris', False)

# Create a ComponentDefinition for each media ingredient in the CSV file

with open('synthetic_complete_ingredients_composition.csv', encoding='utf-8') as media_file:
    csv_reader = csv.reader(media_file)
    next(csv_reader)
    
    for row in csv_reader:
        if len(row[2]) > 0:
            print("ingredient CHEBI ID (row[2]): {}".format(row[2]))
            ingredient = ComponentDefinition(row[0], 'http://purl.obolibrary.org/obo/' + row[2], '1')
        else:
            print("No CHEBI ID")
            ingredient = ComponentDefinition(row[0], 'http://purl.obolibrary.org/obo/OBI_0000079', '1')
            
        print("ingredient_ID: {}".format(row[0]))
        print("ingredient_name: {}".format(row[1]))
        print("Source/Vendor: {}".format(row[3]))
        print("create_unit: {}".format(row[5]))
        print("create_measure: {}".format(row[4]))
        print()
        
        ingredient.name = row[1]
        ingredient.wasDerivedFrom = row[3]

        # Add the media ingredient to the working document

        doc.addComponentDefinition(ingredient)
        
# Create a ModuleDefinition for the composite media and give the role URI for 'culture medium'

media = ModuleDefinition('yg_media_1', '1')
media.name = 'Synthetic Complete'
media.roles = ['http://purl.obolibrary.org/obo/OBI_0000079']

# For each media ingredient in the CSV file, retrieve its ComponentDefinition from the working 
# document and create a FunctionalComponent reference to it in the composite media ModuleDefinition

with open('synthetic_complete_ingredients_composition.csv', encoding='utf-8') as media_file:
    csv_reader = csv.reader(media_file)
    next(csv_reader)
    count = 1 
    for row in csv_reader:
        print(count)

        # Retrieve the media ingredient ComponentDefinition from the working document

        ingred = doc.getComponentDefinition(''.join([getHomespace(), '/', row[0], '/1']))

        # Create a FunctionalComponent reference to the media ingredient ComponentDefinition and
        # label it with the concentration and units

        fc = media.functionalComponents.create(row[0])
        fc.definition = ingred.identity
        if len(row[1]) > 0:
            if len(row[2]) > 0:
                try:
                    print("create_unit: {}".format(row[5]))
                    unit = create_unit(doc, om, row[5])
                    print("Unit: {}".format(unit))
                except:
                    unit = None
                    create_measure(float(row[4]), fc, unit)
                else:
                    create_measure(float(row[4]), fc)
        count += 1

# Add the composite media to the working document

doc.addModuleDefinition(media)

# Write the working document out to an SBOL file

doc.write(os.path.join(os.getcwd(), 'culture_media_1.xml'))