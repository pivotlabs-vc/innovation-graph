#!/usr/bin/env python3

import json
import hashlib
import sys
from rdflib import Literal, URIRef, Graph
import csv

COMMENT=URIRef("http://www.w3.org/2000/01/rdf-schema#comment")
ADVISES=URIRef("http://pivotlabs.vc/innov/t/organisation#")

mappings = {
    "arms-length-body": {
        "arms-length-body": "=consults",
        "committee": "advises",
        "department": "advises",
        "network": "=consults",
        "science-advisory-committee": "-advises",
        "science-advisory-council": "-advises",
        "subcommittee": "advises",
    },
    "committee": {
        "arms-length-body": "-advises",
        "department": "-delegates",
        "science-advisory-committee": "-advises",
    },
    "department": {
        "arms-length-body": "-advises",
        "committee": "delegates",
        "department": "=consults",
        "executive-agency": "-delegates",
        "external-experts": "-advises",
        "group-of-government-experts": "-advises",
        "industrial-council": "-advises",
        "network": "consults",
        "office": "-delegates",
        "profession": "consults",
        "research-centre": "-advises",
        "research-council": "-advises",
        "science-advisory-committee": "-advises",
        "science-advisory-council": "-advises",
    },
    "devolved-administration": {
        "science-advisory-committee": "-advises",
        "arms-length-body": "=consults",
        "network": "consults",
        "science-advisory-council": "-advises",
        "research-centre": "sponsors",
        "executive-agency": "delegates",
    },
    "executive-agency": {
        "science-advisory-committee": "-advises",
    },
    "external-experts": {
        "office": "advises",
        "external-experts": "=consults",
        "science-advisory-committee": "advises",
        "industrial-council": "advises",
        "committee": "advises",
    },
    "industrial-council": {
        "science-advisory-committee": "advises",
    },
    "network": {
        "network": "=consults",
    },
    "office": {
        "profession": "consults",
        "network": "consults",
        "arms-length-body": "-advises",
        "group-of-government-experts": "-advises",
        "office": "=consults",
        "science-advisory-committee": "-advises",
        "science-advisory-council": "-advises",
    },
    "research-centre": {
        "research-centre": "=consults",
        "arms-length-body": "-sponsors",
    },
    "research-council": {
        "research-council": "=consults",
        "executive-agency": "-sponsors",
        "research-centre": "sponsors",
    },
    "science-advisory-committee": {
        "science-advisory-committee": "=advises",
    },
    "science-advisory-council": {
        "science-advisory-council": "=advises",
    },
    "subcommittee": {
        "science-advisory-committee": "-advises"
    }
}

class Edge:
    def __init__(self, data):

        self.id = data["_id"]

class Element:
    def __init__(self, data):

        self.id = data["_id"]
        attrs = data["attributes"]

        self.label = attrs.get("label")
        self.description = attrs.get("description", None)
        self.tags = attrs.get("tags", [])
        self.type = attrs.get("element type", None)
        self.size = attrs.get("size", 0)
        self.betweenness = attrs.get("betweenness", 0)
        self.last = attrs.get("metrics::last", 0)

    def get_type_slug(self):

        map = {
            "Office": "office",
            "Executive Agency": "executive-agency",
            "Research Centre": "research-centre",
            "External Experts": "external-experts",
            "Science Advisory Committee": "science-advisory-committee",
            "Arm's Length Body": "arms-length-body",
            "Network": "network",
            "Department": "department",
            "Science Advisory Council": "science-advisory-council",
            "Research Council": "research-council",
            None: "committee",
            "Subcommittee": "subcommittee",
            "n/a": "committee",
            "Profession": "profession",
            "Industrial Council": "industrial-council",
            "Group of government experts": "group-of-government-experts",
            "Devolved Administration": "devolved-administration",
        }

        return map[self.type]

    def get_id(self):
        return self.get_type_slug() + "/" + self.id

    def hash(self, id):
        return  hashlib.md5(id.encode('utf-8')).hexdigest()[:12]
        
    def get_uri(self):
        hid = self.hash(self.get_id())

        return URIRef(
            "http://pivotlabs.vc/innov/sci-net/" + hid
        )

    def get_type(self):

        return URIRef(
            "http://pivotlabs.vc/innov/t/" + self.get_type_slug()
        )

class Map:
    def __init__(self, elements, edges):
        self.edges = edges
        self.elements = elements

    def get_type(self, type):
        return [
            v
            for v in self.elements.values()
            if v.type == type
        ]

    def get_hierarchy(self, base):

        hier = []
        discovered = set([v.id for v in base])
        tier = 1

        while True:

            discovered_before = len(discovered)
            tier_discovery = set()

            for elt in self.elements.values():

                if elt.id in discovered: continue

                this_tier = False

                for edge in self.edges.values():
                    if edge.src == elt and edge.dest.id in discovered:
                        this_tier = True
                    elif edge.dest == elt and edge.src.id in discovered:
                        this_tier = True

                if this_tier:
                    tier_discovery.add(elt.id)

            tier += 1

            hier.append(
                [self.elements[v] for v in tier_discovery]
            )
            discovered = discovered.union(tier_discovery)

            if len(discovered) == discovered_before:
                break

        return hier

class Project:
    def __init__(self):
        pass

    @staticmethod
    def load(path):

        p = Project()
        p.project = json.load(open(path))
        return p

    def maps(self):
        return {
            map["_id"]: map["name"]
            for map in self.project["maps"]
        }

    def get(self, id):

        m = None
        for map in self.project["maps"]:            
            if map["_id"] == id:
                m = map

        if m == None: raise RuntimeError("No such map")

        all_elements = {
            v["_id"]: v
            for v in self.project["elements"]
        }

        all_edges = {
            v["_id"]: v
            for v in self.project["connections"]
        }

        elements = {}
        for element in m["elements"]:
            id = element["element"]
            elements[id] = Element(all_elements[id])

        edges = {}
        for edge in m["connections"]:
            id = edge["connection"]
            edges[id] = Edge(all_edges[id])
            edges[id].src = elements[all_edges[id]["from"]]
            edges[id].dest = elements[all_edges[id]["to"]]

        return Map(elements, edges)

class Curator:
    def __init__(self, map, schema):
        self.map = map
        self.schema = schema
        self.tiers = self.construct_tiers()

    def construct_tiers(self):

        depts = self.map.get_type("Department")
        hier = self.map.get_hierarchy(depts)

        tiers = {
            v: 0
            for v in depts
        }

        for i in range(0, len(hier)):
            for elt in hier[i]:
                tiers[elt] = i + 1

        return tiers

    def determine_advises_relationship(self, a, b):

        if self.tiers[a] < self.tiers[b]:
            return b, a
        elif self.tiers[b] < self.tiers[a]:
            return a, b
        elif a.betweenness > b.betweenness:
            return b, a
        elif b.betweenness > a.betweenness:
            return a, b

        raise RuntimeError("Cannot determine advises relationship")

    def get_relationship(self, src, dest):
        stype = src.get_type_slug()
        dtype = dest.get_type_slug()

        reln = None
        rev = False

        if stype in mappings:
            if dtype in mappings[stype]:
                reln = mappings[stype][dtype]

        if dtype in mappings:
            if stype in mappings[dtype]:
                reln = mappings[dtype][stype]
                rev = True

        if reln == None:
            raise RuntimeError(
                "No relationship between %s to %s" % (stype, dtype)
            )

        if reln[0] == '-':
            reln = reln[1:]
            rev = not rev

        if reln[0] == '=':
            reln = reln[1:]
            frel = reln
            brel = reln
        else:
            frel = reln
            brel = None

        if rev:
            brel, frel = frel, brel

        return frel, brel
    
    def make_graph(self):

        g = Graph()

        for elt in self.map.elements.values():

            g.add((
                elt.get_uri(),
                URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
#                elt.get_type(),
                URIRef(self.schema.map("schema:Organization")),
            ))

            g.add((
                elt.get_uri(),
                URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
                Literal(elt.label),
            ))

            if elt.description:
                g.add((
                    elt.get_uri(),
                    COMMENT,
                    Literal(elt.description)
                ))

        for edge in self.map.edges.values():

            fwd, rev = self.get_relationship(edge.src, edge.dest)

            if fwd:
                g.add((
                    edge.src.get_uri(),
                    ADVISES + fwd,
                    edge.dest.get_uri(),
                ))

            if rev:
                g.add((
                    edge.dest.get_uri(),
                    ADVISES + rev,
                    edge.src.get_uri(),
                ))

        return g

    def make_table(map):

        # FIXME: Did nothing with tiers

        table = []

        for v in map.edges.values():

            src = v.src
            dest = v.dest

            row = (
                src.label, src.description, src.type,
                dest.label, dest.description, dest.type
            )

            table.append(row)

        return table

    def write_csv(map):

        tbl = make_table(map)

        writer = csv.writer(sys.stdout)

        for row in tbl:
            writer.writerow(row)

    @staticmethod
    def process(subdir, metadata, schema):

        p = Project.load(subdir + "/" + "science-networks.json")
        m = p.get("map-1vlBsQ28")

        c = Curator(m, schema)

        g = c.make_graph()

        return g

