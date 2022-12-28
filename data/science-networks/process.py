#!/usr/bin/env python3

import json
import sys
from rdflib import Literal, URIRef, Graph
import csv
import logging

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
        "department": "parent",
        "science-advisory-committee": "-advises",
    },
    "department": {
        "arms-length-body": "-advises",
        "committee": "-parent",
        "department": "=consults",
        "executive-agency": "-parent",
        "external-experts": "-advises",
        "group-of-government-experts": "-advises",
        "industrial-council": "-advises",
        "network": "consults",
        "office": "-parent",
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
        "executive-agency": "-parent",
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
            "Subcommittee": "subcommittee",
            "Profession": "profession",
            "Industrial Council": "industrial-council",
            "Group of government experts": "group-of-government-experts",
            "Devolved Administration": "devolved-administration",

            # Assert it's a committe if type wasn't recorded
            "n/a": "committee",
            None: "committee",
        }

        return map[self.type]

    def get_id(self):
        id = self.label
        id = id.replace(" - ", "-")
        id = id.replace(" ", "-")
        id = id.lower()
        return id
        
    def get_uri(self):

        id = self.get_id()

        return URIRef(
            "http://pivotlabs.vc/innov/organisation/" + id
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
                elt.get_type(),
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

                if fwd == "parent":
                    fwd = URIRef(self.schema.map("schema:parentOrganization"))
                else:
                    fwd = ADVISES + fwd

                g.add((
                    edge.src.get_uri(),
                    fwd,
                    edge.dest.get_uri(),
                ))

            if rev:

                if rev == "parent":
                    rev = URIRef(self.schema.map("schema:parentOrganization"))
                else:
                    rev = ADVISES + rev

                g.add((
                    edge.dest.get_uri(),
                    rev,
                    edge.src.get_uri(),
                ))

        return g

    @staticmethod
    def process(subdir, metadata, schema):

        path = subdir + "/" + "science-networks.json"
        logging.info(f"  Loading network...")
        p = Project.load(subdir + "/" + "science-networks.json")

        logging.info("  Get map...")
        m = p.get("map-1vlBsQ28")

        logging.info("  Create graph...")
        c = Curator(m, schema)
        g = c.make_graph()
        logging.info("  Graph creation complete")

        return g

