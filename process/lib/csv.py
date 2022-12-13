
# Handle CSV input

from rdflib import Graph
import csv
import hashlib

from . exceptions import *

def hash(x):
    return hashlib.md5(x.encode('utf-8')).hexdigest()[:12]

class Row:
    def __init__(self, row, fields):
        self.row = row
        self.fields = fields
    def get(self, id):
        if id not in self.fields:
            raise RuntimeError("No such field " + id)
        return self.row[self.fields[id]]

class Table:

    def __init__(self, path, fields=None, use_header=False, skip=0):

        f = open(path)
        self.table = csv.reader(f)

        self.line = 0

        if use_header:
            flds = next(self.table)
            self.line += 1
        else:
            flds = fields
        fmap = {}

        for i in range(0, len(flds)):
            fmap[flds[i]] = i

        self.fields = fmap

        for i in range(0, skip):
            self.line += 1
            row = next(self.table)

    def __next__(self):

        row = next(self.table)

        self.line += 1

        if len(row) != len(self.fields):
            raise LineProcessingError(
                path, self.line,
                f"CSV row has {len(row)} cells, mismatches the field list"
            )

        return Row(row, self.fields)

    def __iter__(self):
        return self

class LiteralField:
    def __init__(self, props, schema):

        self.schema = schema

        if "ignore" in props:
            self.ignore = props["ignore"]
        else:
            self.ignore = {}

        self.pred = schema.map(props["predicate"])
        self.field = props["object-field"]

        if "map" in props:
            self.mapping = props["map"]
        else:
            self.mapping = None

        if "datatype" in props:
            self.datatype = props["datatype"]
        else:
            self.datatype = None

    def handle(self, identity, row):

        value = row.get(self.field)
        raw = value

        if value in self.ignore: return []

        if self.mapping:
            if value not in self.mapping:
                return []
            else:
                value = self.mapping[value]

        if self.datatype:
            obj = self.schema.map(value, self.datatype)
        else:
            obj = self.schema.map(value)

        return [(identity, self.pred, obj)]

class ClassField:
    def __init__(self, props, schema):

        self.schema = schema

        if "ignore" in props:
            self.ignore = props["ignore"]
        else:
            self.ignore = {}

        self.pred = schema.map(props["predicate"])
        self.field = props["object-field"]

        if "map" in props:
            self.mapping = props["map"]
        else:
            self.mapping = None

        if "derive-object-id" in props and props["derive-object-id"]:
            self.id_prefix = props["object-id-prefix"]
            self.derive_id = True
        else:
            self.derive_id = False

        if "use-object-id-hash" in props and props["use-object-id-hash"]:
            self.id_prefix = props["object-id-prefix"]
            self.use_id_hash = True
        else:
            self.use_id_hash = False


        self.object_type = schema.map(props["object-type"])

    def handle(self, identity, row):

        value = row.get(self.field)
        raw = value

        if value in self.ignore: return []

        if self.mapping:
            if value not in self.mapping:
                return []
            else:
                value = self.mapping[value]

        if self.derive_id:
            value = value.replace(" ", "-")
            value = value.lower()
            value = self.id_prefix + value
        elif self.use_id_hash:
            value = hash(value)
            value = self.id_prefix + value

        obj = self.schema.map(value)

        return [
            (identity, self.pred, obj),
            (obj, self.schema.map("rdf:type"), self.object_type),
            (obj, self.schema.map("rdfs:label"), self.schema.map(raw))
        ]

class Obj:
    def __init__(self, props, schema):

        self.schema = schema

        if "id-prefix" in props:
            self.id_prefix = props["id-prefix"]
        else:
            self.id_prefix = None

        if "class" not in props:
            raise MetadataError(
                subdir, "The 'object.class' field does not exist"
            )

        self.id_field = props["id-field"]

        self.cls = schema.map(props["class"])

        self.properties = []

        for prop in props["properties"]:
            if "object-type" in prop:
                self.properties.append(ClassField(prop, schema))
            else:
                self.properties.append(LiteralField(prop, schema))

    def handle(self, row):

        identity = row.get(self.id_field)
        if self.id_prefix:
            identity = self.id_prefix + identity
            identity = self.schema.map(identity)

        tpls = [
            (identity, self.schema.map("rdf:type"), self.cls)
        ]

        for prop in self.properties:
            tpls.extend(prop.handle(identity, row))

        return tpls

class Csv:

    @staticmethod
    def load(subdir, metadata, schema):

        g = Graph()

        if "input" not in metadata:
            raise MetadataError(subdir, "The 'input' field does not exist")

        if "fields-from-header" in metadata and metadata["fields-from-header"]:
            from_header = True
        else:
            from_header = False

        if not from_header:
            if "fields" not in metadata:
                raise MetadataError(subdir, "The 'fields' field does not exist")
            fields = metadata["fields"]
        else:
            fields = None

        if "skip" in metadata:
            skip = int(metadata["skip"])
        else:
            skip = 0

        tbl = Table(
            subdir + "/" + metadata["input"], fields=fields,
            use_header=from_header, skip=skip
        )
        
        if "object" not in metadata:
            raise MetadataError(subdir, "The 'object' field does not exist")

        object = metadata["object"]

        obj = Obj(object, schema)

        for row in tbl:

            tpls = obj.handle(row)
            for tpl in tpls:
                g.add(tpl)

        c = Csv()
        c.graph = g
        return c

