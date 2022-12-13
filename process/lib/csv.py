
# Handle CSV input

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

      if "object" not in metadata:
         raise MetadataError(subdir, "The 'object' field does not exist")

      object = metadata["object"]

      if "id-prefix" in object:
         id_prefix = object["id-prefix"]
      else:
         id_prefix = None

      if "skip" in metadata:
         skip = int(metadata["skip"])
      else:
         skip = 0

      
      if "fields-from-header" in metadata:
         if metadata["fields-from-header"]:
            fields_from_header = True
         else:
            fields_from_header = False
      else:
         fields_from_header = False

      if not fields_from_header:
         if "fields" not in metadata:
            raise MetadataError(subdir, "The 'fields' field does not exist")
         fields = metadata["fields"]

      path = subdir + "/" + metadata["input"]

      if "class" not in object:
         raise MetadataError(subdir, "The 'object.class' field does not exist")

      cls = URIMapping.map(object["class"])

      with open(path) as f:

         reader = csv.reader(f)
         line = 1

         for row in reader:

            if fields_from_header:
               fields = row
               fields_from_header = False
               continue

            if skip > 0:
               skip -= 1
               continue

            if len(row) != len(fields):
               raise LineProcessingError(
                  path, line,
                  f"CSV row has {len(row)} cells, mismatches the field list"
               )

            f = {}
            for i in range(0, len(row)):
               f[fields[i]] = row[i]

            identity = f[object["id-field"]]
            if id_prefix:
               identity = id_prefix + identity
            identity = URIMapping.map(identity)

            g.add((identity, URIMapping.map("rdf:type"), cls))

            for prop in object["properties"]:

               pred = URIMapping.map(prop["predicate"])

               if "datatype" in prop:
                  obj = URIMapping.map(f[prop["object-field"]], prop["datatype"])
               else:
                  obj = URIMapping.map(f[prop["object-field"]])

               g.add((identity, pred, obj))

            line += 1

      c = Csv()
      c.graph = g
      return c
