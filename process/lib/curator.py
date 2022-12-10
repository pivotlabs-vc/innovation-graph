
#
# Curator class, handles schema loading invocation of the data processing on
# each directory, and returns a graph.
#

import os
import json
import logging

from . csv import *
from . turtle import *
from . schema import *

# This is the list of processors currently supported.  To add a new processing
# type create a class and add it to this dict.
processors = {
    "csv": Csv,
    "turtle": Turtle,
}

# Curator class
class Curator:

    # Init, empty schema
    def __init__(self):
        self.schema = None

    # Loads the schema, Turtle format
    def load_schema(self, path):
        self.schema = Schema.load(path)

    # Processes a subdirectory
    def process(self, subdir):

        logging.info("Processing " + subdir + "...")
        metadata = json.load(open(subdir + "/metadata.json"))
        for field in [
                "id", "description", "contributors", "origin", "copyright",
                "processing"
        ]:
            if field not in metadata:
                raise MetadataError(
                    subdir, f"The '{field}' field does not exist"
                )

        if metadata["processing"] not in processors:
            msg = f"Processing type '{metadata['processing']}' not known."
            raise MetadataError(subdir, msg)
   
        cls = processors[metadata["processing"]]

        return cls.load(subdir, metadata, self.schema)

    # Walks a directory searching for sub-directories with metadata.json
    # files
    def walk(self, dir):

        g = Graph()

        # Add the schema to our output graph
        for tpl in self.schema.graph:
            g.add(tpl)

        for subdir, dirs, files in os.walk(dir):

            # Any sub-directory with a metadata.json file is processed
            ix_path = subdir + "/metadata.json"

            # Ignore directories with no metadata.json
            if not os.path.exists(ix_path):
                continue

            # Invoke processing
            sg = self.process(subdir)

            # Add the sub-graph to the conglomerate graph
            for tpl in sg.graph:
                g.add(tpl)

        return g

