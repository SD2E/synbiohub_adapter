from fetch_SPARQL import fetch_SPARQL

server = "http://hub-api.sd2e.org:80/sparql"

# A collection aggregates all objects associated with a challenge problem or experiment plan

collection = '<http://hub.sd2e.org/user/nicholasroehner/rule_30/rule_30_collection/1>'

# Retrieves all circular DNA from specified collection

plasmid_query = ["PREFIX sbol: <http://sbols.org/v2#> "]
plasmid_query.append("SELECT ?plasmid WHERE { ")
plasmid_query.append(collection + " sbol:member ?plasmid . ?plasmid sbol:type ?type1, ?type2 . ")
plasmid_query.append("FILTER ( ?type1 = <http://www.biopax.org/release/biopax-level3.owl#DnaRegion> && ?type2 = <http://identifiers.org/so/SO:0000988> ) }")

plasmid_metadata = fetch_SPARQL(server, ''.join(plasmid_query))

print(plasmid_metadata)

# Retrieves all small molecule inducers from specified collection

inducer_query = ["PREFIX sbol: <http://sbols.org/v2#> "]
inducer_query.append("SELECT ?inducer WHERE { ")
inducer_query.append(collection + " sbol:member ?inducer . ?inducer sbol:type ?type; sbol:role ?role . ")
inducer_query.append("FILTER ( ?type = <http://www.biopax.org/release/biopax-level3.owl#SmallMolecule> && ?role = <http://identifiers.org/chebi/CHEBI:35224> ) }")

inducer_metadata = fetch_SPARQL(server, ''.join(inducer_query))

print(inducer_metadata)

# Retrieves all samples and associated experimental conditions from specified collection

sample_query = ["PREFIX sbol: <http://sbols.org/v2#> "]
sample_query.append("PREFIX sd2: <http://sd2e.org#> ")
sample_query.append("SELECT ?sample ?condition WHERE { ")
sample_query.append(collection + " sbol:member ?sample ; sbol:member ?condition . ?sample sd2:built ?condition }")

sample_metadata = fetch_SPARQL(server, ''.join(sample_query))


print(sample_metadata)