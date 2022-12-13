
# Hearistic mapping of a string to either a URIRef or Literal depending on
# whether it looks like a URL or not.

from rdflib import Literal, URIRef

# Set of namespace prefixes supported
namespaces = {
   "dc": "http://purl.org/dc/elements/1.1/",
   "property": "http://pivotlabs.vc/challenges/p#",
   "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
   "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
   "type": "http://pivotlabs.vc/challenges/t#",
   "source": "http://pivotlabs.vc/challenges/s/",
   "person": "http://pivotlabs.vc/challenges/p/",
   "xsd": "http://www.w3.org/2001/XMLSchema#",
}

class URIMapping:

   # Prefix mapping
   @staticmethod
   def map_ns(str):
      if str.startswith("http://"): return str
      if str.startswith("https://"): return str
      ix = str.find(":")
      if ix < 0: return str
      ns = str[0:ix]
      if ns not in namespaces: return str
      return namespaces[ns] + str[ix + 1:]

   # Map prefix, if it exists and return either URIRef or Literal
   @staticmethod
   def map(str, tp=None):
      str = URIMapping.map_ns(str)
      if str.startswith("http:"):
         return URIRef(str)
      if str.startswith("https:"):
         return URIRef(str)

      if tp:
         tp = URIMapping.map_ns(tp)
         return Literal(str, datatype=tp)
      return Literal(str)

  
