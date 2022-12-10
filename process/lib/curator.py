
import os
import json
import logging

from . csv import *
from . turtle import *
from . schema import *

class Curator:
   
    processors = {
        "csv": Csv,
        "turtle": Turtle,
    }

    def __init__(self):

        self.schema = None

    def load_schema(self, path):

        self.schema = Schema.load(path)

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

        if metadata["processing"] not in Curator.processors:
            msg = f"Processing type '{metadata['processing']}' not known."
            raise MetadataError(subdir, msg)
   
        cls = Curator.processors[metadata["processing"]]

        return cls.load(subdir, metadata, self.schema)
   
    def walk(self, dir):

        g = Graph()

        for tpl in self.schema.graph:
            g.add(tpl)

        for subdir, dirs, files in os.walk(dir):
   
            ix_path = subdir + "/metadata.json"

            if not os.path.exists(ix_path):
                continue

            sg = self.process(subdir)

            for tpl in sg.graph:
                g.add(tpl)

        return g

