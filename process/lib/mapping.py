
# Hearistic mapping of a string to either a URIRef or Literal depending on
# whether it looks like a URL or not.

from rdflib import Literal, URIRef
import json

# Set of namespace prefixes supported
namespaces = json.load(open("schema/namespaces.json"))

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

  
