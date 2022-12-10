
from rdflib import Graph

from . defs import *

class Schema:

   def __init__(self):
      self.properties = {}
      self.classes = {}

   @staticmethod
   def load(path):

      s = Schema()

      g = Graph()
      g.parse(path, format="turtle")

      s.graph = g

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
