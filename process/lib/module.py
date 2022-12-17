
# Handle module input

from rdflib import Graph
import importlib

from . exceptions import *

class Module:
   @staticmethod
   def load(subdir, metadata, schema):

      if "module" not in metadata:
         raise MetadataError(subdir, "The 'module' field does not exist")

      ep = metadata.get("entrypoint", "process")

      t = Module()

      path = subdir + "/" + metadata["module"]

      mod = importlib.machinery.SourceFileLoader("process", path).load_module()

      fn = mod

      for v in ep.split("."):
         try:
            fn = getattr(fn, v)
         except:
            raise RuntimeError("Couldn't find entrypoint '%s'" % ep)

      g = fn(subdir, metadata, schema)
      
      

      for (s, p, o) in g:
         if p not in schema.properties:
            if p not in schema.classes:
               raise PredicateNotKnown(path, p, "Not known: " + str(p))

      t.graph = g

      return t

