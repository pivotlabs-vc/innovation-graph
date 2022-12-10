
from rdflib import Literal, URIRef

namespaces = {
   "dc": "http://purl.org/dc/elements/1.1/",
   "property": "http://pivotlabs.vc/challenges/p#",
   "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
   "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
   "type": "http://pivotlabs.vc/challenges/",
   "source": "http://pivotlabs.vc/challenges/s/",
}

class URIMapping:

   @staticmethod
   def map_ns(str):
      if str.startswith("http://"): return str
      if str.startswith("https://"): return str
      ix = str.find(":")
      if ix < 0: return str
      ns = str[0:ix]
      if ns not in namespaces: return str
      return namespaces[ns] + str[ix + 1:]

   @staticmethod
   def map(str):
      str = URIMapping.map_ns(str)
      if str.startswith("http:"):
         return URIRef(str)
      if str.startswith("https:"):
         return URIRef(str)
      return Literal(str)

  
