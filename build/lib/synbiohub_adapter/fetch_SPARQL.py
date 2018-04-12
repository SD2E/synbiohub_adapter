#!/usr/bin/python

from SPARQLWrapper import SPARQLWrapper, JSON

def fetch_SPARQL(server, query):
	sparql = SPARQLWrapper(server)
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results