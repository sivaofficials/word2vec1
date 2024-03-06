from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

from urllib.parse import urlparse
import requests
import re

class DBpedia: 

    @staticmethod
    def check_seed(seed_word):
        result = requests.get(f"http://dbpedia.org/resource/{seed_word}")
        return result.status_code
    
    @staticmethod
    def layer1(seed_word):
        dbo = Namespace("http://dbpedia.org/ontology/")
        g = Graph()    
        dbpedia_url = f"http://dbpedia.org/resource/{seed_word}"
        try:
            g.parse(dbpedia_url)
        except Exception as e:
            print(f"Error parsing RDF data from {dbpedia_url}: {e}")
        terms_layer1 = set()
        query_str = f"""
            SELECT ?linkedResource WHERE {{
                <{dbpedia_url}> dbo:wikiPageWikiLink ?linkedResource.
            }}
        """
        query = prepareQuery(query_str, initNs={"dbo": dbo})
        terms_layer1.update([str(row.linkedResource) for row in g.query(query)])
        return terms_layer1
    
    @staticmethod
    def layer2(seed_url):
        dbo = Namespace("http://dbpedia.org/ontology/")

        g = Graph()
        try:
            g.parse(seed_url)
        except Exception as e:
            print(f"Error parsing RDF data from {seed_url}: {e}")

        terms_layer = set()
        query_str = f"""
            SELECT ?linkedResource WHERE {{
                <{seed_url}> dbo:wikiPageWikiLink ?linkedResource.
            }}
        """
        query = prepareQuery(query_str, initNs={"dbo": dbo})
        terms_layer.update([str(row.linkedResource) for row in g.query(query)])
        return terms_layer

    @staticmethod
    def satisation(refined_layer):
        pattern = r'\b(?![0-9_])[A-Za-z_]{8,15}\b|\b(?![0-9_])[A-Za-z_]{4,}\b'
        with open(refined_layer, "r") as file:
            content = file.read()  
            matches = re.findall(pattern, content)  
        unique_matches = set(matches)
        return unique_matches
    
