"""

"""

from SPARQLWrapper import SPARQLWrapper, JSON
from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch(['http://elastic:WrVChWeyZ8PMWrawdtu4cc2R23JZy79x@hub-search.sd2e.org:9200'])
host = "https://hub-api.sd2e.org/sparql"

sparql = SPARQLWrapper(host)

def virtuoso_to_elasticsearch_full(step=1000):
  sparql.setQuery("""
  SELECT COUNT DISTINCT *
  WHERE {{
    GRAPH <http://hub.sd2e.org/user/sd2e> {{ ?s [] ?o }}
  }}""")

  sparql.setReturnFormat(JSON)
  num_triples = int(sparql.query().convert()['results']['bindings'][0]['callret-0']['value'])

  docs = set()

  for offset in range(0, num_triples, step):
    sparql.setQuery("""
    SELECT DISTINCT *
    WHERE {{
      GRAPH <http://hub.sd2e.org/user/sd2e> {{ ?s [] ?o }}
    }} LIMIT {} OFFSET {}""".format(step, offset))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    def extract_uri_parts(uri):
      parts = [u"{}".format(p) for p in v['value'].split('/') if p and p not in {'http:', 'https:'}]
      bits = []
      for p in parts:
        bits.extend(p.split('_'))
      return list(set(parts + bits))

    these_docs = []
    for r in results:
      for k, v in r.iteritems():
        these_docs.append(u'{{ "{}": "{}", "parts": {} }}'.format(v['type'], v['value'],
            json.dumps(extract_uri_parts(v['value']))))

    docs.update(these_docs)


  actions = []
  id = 0

  for d in docs:
    actions.append({
      '_index': 'sd2e',
      '_type': 'document',
      '_id': id,
      '_source': json.loads(d)
    })
    id += 1

  helpers.bulk(es, actions)


def find_entities(input):
  results = es.search(index='sd2e', body={'query': {'multi_match': {'query': input, "fuzziness": "AUTO", 'fields': ['parts', 'uri', 'literal']}}})
  results = set([u'{{"{}": "{}"}}'.format(k, item['_source'][k]) for item in results['hits']['hits'] for k in item['_source'] if k != 'parts'])
  results = [json.loads(s) for s in results]
  return results



