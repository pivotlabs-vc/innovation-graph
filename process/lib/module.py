
# Handle module input

from rdflib import Graph
import importlib

from . exceptions import *

class Module:
   @staticmethod
   def load(subdir, metadata, schema):

      if "module" not in metadata:
         raise MetadataError(subdir, "The 'module' field does not exist")

      t = Module()

#      g = Graph()

      path = subdir + "/" + metadata["module"]

#      mod = importlib.import_module(path)
      mod = importlib.machinery.SourceFileLoader("process", path).load_module()

      g = mod.process(subdir, metadata, schema)
      
      

      for (s, p, o) in g:
         if p not in schema.properties:
            if p not in schema.classes:
               raise PredicateNotKnown(path, p, "Not known: " + str(p))

      t.graph = g

      return t

