import argparse
import csv
import sys
import os
from pySBOLx.pySBOLx import XDocument

SD2_DESIGN_NS = 'http://hub.sd2e.org/user/sd2e/design'
CHEBI_NS = 'http://identifiers.org/chebi/'

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='*', default=[f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')])
    parser.add_argument('-o', '--output', nargs='?', default='generated_sbol.xml')
    parser.add_argument('-m', '--om', nargs='?', default=os.path.join(os.getcwd(), 'om-2.0.rdf'))
    args = parser.parse_args(args)

    doc = generate_sbol(args.input, args.om)
    
    doc.write(args.output)

def generate_sbol(csv_files, om_file=None):
    doc = XDocument()
    doc.configure_options(SD2_DESIGN_NS, False, False)

    if om_file is None:
        try:
            om = doc.read_om(os.path.join(os.getcwd(), 'om-2.0.rdf'))
        except:
            om = None
    else:
        om = doc.read_om(om_file)

    generate_device_switcher = {
        'CHEBI': generate_chebi,
        'DNA': generate_dna,
        'Enzyme': generate_enzyme,
        'Plasmid': generate_plasmid,
        'Protein': generate_protein,
        'RNA': generate_rna,
        'Strain': generate_strain,
        'Media': generate_media
    }

    generate_system_switcher = {
        'Gate': generate_gate, 
        'Media': generate_media
    }

    generate_input_switcher = {
        'Inducer': generate_inducer
    }
    
    for csv_file in csv_files:
        generate_sbol_helper(doc, csv_file, generate_device_switcher, generate_system_switcher, generate_input_switcher, om)

    return doc

def generate_sbol_helper(doc, csv_file, generate_device_switcher, generate_system_switcher, generate_input_switcher, om=None, out_devices=[], out_systems=[], out_inputs=[], out_measures={}):
    with open(csv_file) as csv_content:
        csv_reader = csv.reader(csv_content)
        header = {k: v for v, k in enumerate(next(csv_reader))}

        for row in csv_reader:
            generate_type = row[header['Type']]

            try:
                generate_system = generate_system_switcher[generate_type]

                devices = []
                systems = []
                inputs = []
                measures = {}

                try:
                    aux_file = row[header['Composition_File']]

                    generate_sbol_helper(doc, aux_file, generate_device_switcher, generate_system_switcher, generate_input_switcher, om, devices, systems, inputs, measures)
                except:
                    pass

                identified = generate_system(doc, row, header, devices, systems, inputs, measures)

                out_systems.append(identified)
            except:
                try:
                    generate_device = generate_device_switcher[generate_type]

                    identified = generate_device(doc, row, header)

                    out_devices.append(identified)
                except:
                    generate_input = generate_input_switcher[generate_type]

                    identified = generate_input(doc, row, header)

                    out_inputs.append(identified)

            conc = generate_concentration(doc, row, header, om)
            
            if conc is not None:
                out_measures[identified.displayId] = conc

def generate_concentration(doc, row, header, om):
    try:
        unit = generate_unit(doc, row, header, om)

        return {'mag': float(row[header['Concentration']]), 'unit': unit, 'id': 'concentration'}
    except:
        try:
            return {'mag': float(row[header['Concentration']]), 'id': 'concentration'}
        except:
            return None

def generate_chebi(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('chebi ' + display_id)

    return doc.create_component_definition(display_id, name, descr, CHEBI_NS + row[header['CHEBI']])

def generate_media(doc, row, header, devices=[], systems=[], inputs=[], measures={}):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('media ' + display_id)

    return doc.create_media(devices, systems, inputs, measures, display_id, name, descr)

def generate_dna(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('dna ' + display_id)

    return doc.create_dna(display_id, name, descr)

def generate_enzyme(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('enzyme ' + display_id)

    return doc.create_enzyme(display_id, name, descr)

def generate_gate(doc, row, header, devices=[], systems=[], inputs=[], measures={}):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('gate ' + display_id)

    return doc.create_gate(devices, systems, inputs, measures, display_id, name, descr)

def generate_inducer(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('inducer ' + display_id)

    return doc.create_inducer(display_id, name, descr)

def generate_plasmid(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('plasmid ' + display_id)

    return doc.create_plasmid(display_id, name, descr)

def generate_protein(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('protein ' + display_id)

    return doc.create_protein(display_id, name, descr)

def generate_rna(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('rna ' + display_id)

    return doc.create_rna(display_id, name, descr)

def generate_strain(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('strain ' + display_id)

    return doc.create_strain(display_id, name, descr)

def generate_unit(doc, row, header, om):
    symbol = row[header['Concentration_Units']]

    try:
        return doc.create_unit(om, symbol)
    except:
        return doc.create_unit(om=om, name=symbol)

if __name__ == '__main__':
    main()