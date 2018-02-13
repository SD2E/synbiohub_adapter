from fetch_SPARQL import fetch_SPARQL

server = "http://hub-api.sd2e.org:80/sparql"

# A collection aggregates all objects associated with a challenge problem or experiment plan

collection = '<http://hub.sd2e.org/user/nicholasroehner/rule_30/rule_30_collection/1>'

# Retrieves all circular DNA from specified collection
# (Double braces get converted to single braces, since we're using format)
plasmid_query = """
PREFIX sbol: <http://sbols.org/v2#> 
SELECT ?plasmid WHERE {{ 
  {col} sbol:member ?plasmid .
  ?plasmid sbol:type ?type1, ?type2 .
  FILTER ( ?type1 = <http://www.biopax.org/release/biopax-level3.owl#DnaRegion> && ?type2 = <http://identifiers.org/so/SO:0000988> ) 
}}
""".format(col=collection)

plasmid_metadata = fetch_SPARQL(server, plasmid_query)

print(plasmid_metadata)

# Retrieves all small molecule inducers from specified collection

inducer_query = """
PREFIX sbol: <http://sbols.org/v2#> 
SELECT ?inducer WHERE {{
  {col} sbol:member ?inducer .
  ?inducer sbol:type ?type;
           sbol:role ?role .
  FILTER ( ?type = <http://www.biopax.org/release/biopax-level3.owl#SmallMolecule> && ?role = <http://identifiers.org/chebi/CHEBI:35224> )
}}""".format(col=collection)

inducer_metadata = fetch_SPARQL(server, inducer_query)

print(inducer_metadata)

# Retrieves all samples and associated experimental conditions from specified collection

sample_query = """
PREFIX sbol: <http://sbols.org/v2#>
PREFIX sd2: <http://sd2e.org#>
SELECT ?sample ?condition WHERE {{
  {col} sbol:member ?sample ;
        sbol:member ?condition .
  ?sample sd2:built ?condition
}}""".format(col=collection)

sample_metadata = fetch_SPARQL(server, sample_query)


print(sample_metadata)