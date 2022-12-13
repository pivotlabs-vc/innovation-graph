
# Loads schema and maintains sets of properties and classes

from rdflib import Literal, URIRef, Graph
import json

from . defs import *

class Schema:

    def __init__(self):
       self.properties = {}
       self.classes = {}

    @staticmethod
    def load(path):

        s = Schema()

        g = Graph()
        g.parse(path + "/schema.ttl", format="turtle")

        s.graph = g
        s.namespaces = json.load(open(path + "/namespaces.json"))

        for tpl in g:
            if len(tpl) != 3:
                raise RuntimeError("Schema parsing unexpected triple failure")

            if tpl[1] == DESCRIPTION:
                pass
            if tpl[1] == LABEL:
                pass
            if tpl[1] == IS_A:
                if tpl[2] == PROPERTY:
                    s.properties[tpl[0]] = True
                if tpl[2] == CLASS:
                    s.classes[tpl[0]] = True

        s.properties[LABEL] = True
        s.properties[IS_A] = True

        return s

    # Prefix mapping
    def map_ns(self, str):
        if str.startswith("http://"): return str
        if str.startswith("https://"): return str
        ix = str.find(":")
        if ix < 0: return str
        ns = str[0:ix]
        if ns not in self.namespaces: return str
        return self.namespaces[ns] + str[ix + 1:]

    # Map prefix, if it exists and return either URIRef or Literal
    def map(self, str, tp=None):
        str = self.map_ns(str)
        if str.startswith("http:"):
            return URIRef(str)
        if str.startswith("https:"):
            return URIRef(str)

        if tp:
            tp = self.map_ns(tp)
            return Literal(str, datatype=tp)
        return Literal(str)

  
