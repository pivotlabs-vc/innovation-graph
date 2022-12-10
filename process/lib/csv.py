
from rdflib import Graph
import csv

from . mapping import *
from . exceptions import *

class Csv:

   @staticmethod
   def load(subdir, metadata, schema):

      g = Graph()

      if "input" not in metadata:
         raise MetadataError(subdir, "The 'input' field does not exist")

      if "fields" not in metadata:
         raise MetadataError(subdir, "The 'fields' field does not exist")

      if "id-prefix" not in metadata:
         raise MetadataError(subdir, "The 'id-prefix' field does not exist")

      path = subdir + "/" + metadata["input"]
      fields = metadata["fields"]
      prefix = metadata["id-prefix"]

      if len(fields) < 2:
         raise MetadataError(
            subdir, "Fields list must have at least 2 elements"
         )

      if fields[0] != "%%identity%%":
         raise MetadataError(
            subdir, "%%identity%% must be first element of fields list"
         )

      with open(path) as f:

         reader = csv.reader(f)
         line = 1

         for row in reader:

            if len(row) != len(fields):
               raise LineProcessingError(
                  path, line,
                  f"CSV row has {len(row)} cells, mismatches the field list"
               )

            triples = []
            for i in range(1, len(row)):
               s = URIMapping.map(prefix + row[0])
               p = URIMapping.map(fields[i])
               o = URIMapping.map(row[i])

               if p not in schema.properties:
                  if  p not in schema.classes:
                     raise PredicateNotKnown(path, p, "Not known: " + str(p))

               g.add((s, p, o))

            line += 1

      c = Csv()
      c.graph = g
      return c
