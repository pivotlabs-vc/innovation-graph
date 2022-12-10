
# Handle Turtle input

from rdflib import Graph

from . exceptions import *

class Turtle:
   @staticmethod
   def load(subdir, metadata, schema):

      if "input" not in metadata:
         raise MetadataError(subdir, "The 'input' field does not exist")

      t = Turtle()

      g = Graph()

      path = subdir + "/" + metadata["input"]
      g.parse(source=open(path), format="turtle")

      for (s, p, o) in g:
         if p not in schema.properties:
            if p not in schema.classes:
               raise PredicateNotKnown(path, p, "Not known: " + str(p))

      t.graph = g

      return t
