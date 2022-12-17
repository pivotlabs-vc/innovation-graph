#!/usr/bin/env python3

import json
import hashlib
import sys
from rdflib import Literal, URIRef, Graph
import csv

DESCRIPTION=URIRef("http://pivotlabs.vc/challenges/p#description")
ADVISES=URIRef("http://pivotlabs.vc/challenges/p#advises")

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
            "http://pivotlabs.vc/challenges/gos/" + hid
        )

    def get_type(self):

        return URIRef(
            "http://pivotlabs.vc/challenges/t#" + self.get_type_slug()
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

def construct_tiers(m):

    depts = m.get_type("Department")
    hier = m.get_hierarchy(depts)

    tier = {
        v: 0
        for v in depts
    }

    for i in range(0, len(hier)):
        for elt in hier[i]:
            tier[elt] = i + 1

    return tier

def determine_advises_relationship(tiers, a, b):
    
    if tiers[a] < tiers[b]:
        return b, a
    elif tiers[b] < tiers[a]:
        return a, b
    elif a.betweenness > b.betweenness:
        return b, a
    elif b.betweenness > a.betweenness:
        return a, b

    raise RuntimeError("Cannot determine advises relationship")

def make_graph(map):

    tiers = construct_tiers(map)

    g = Graph()

    for elt in map.elements.values():

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
                DESCRIPTION,
                Literal(elt.description)
            ))

    for edge in map.edges.values():

        try:
            a, b = determine_advises_relationship(tiers, edge.src, edge.dest)
        except:

            # No advises relationship, ignore this edge
            continue

        g.add((
            a.get_uri(),
            ADVISES,
            b.get_uri(),
        ))

    return g

def make_table(map):

    tiers = construct_tiers(map)

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

def process(subdir, metadata, schema):

    p = Project.load(subdir + "/" + "science-networks.json")
    m = p.get("map-1vlBsQ28")

    g = make_graph(m)

    return g

