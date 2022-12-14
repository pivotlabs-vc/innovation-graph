
# Crash course in knowledge graph concepts

## Facts

The knowledge graph represents a collection of assertions of facts.
By way of example, this document starts with a collection of facts about my
cats:

- Fred lives with Hope
- Fred is a cat
- Fred has 4 legs

## Predicates

In English grammar, facts can commonly be seen structured as subject, verb,
object.  But verbs don't always work the way that we want them to
for representing knowledge.  Instead of recording that:

> Fred (subject) has (verb) 4 legs (object)

I want to say that

> Fred (subject) has legs (verb) 4

Hence we'll talk about predicates rather than verbs.

In an RDF knowledge graph, facts are triples: subject, predicate,
object.

## Entity references

All the things that get described in a knowledge graph are entities.
Entities need a unique reference.  Fred is the name of my cat, but
also the name of several other people in my street: to make it clear
which entity is in use, a unique reference is needed for every entity.

In RDF, that reference is presented as a URL.  It is normal to include
the name of the organisation creating the graph and enough components
to make the URL clear and unique.  So my cat Fred can be
`http://pivotlabs.vc/animals/fred`.  Because we're using a URL, it looks
like the sort of thing you could put in a browser.  But the URL doesn't
have to point to an actual web page or resource.  It can, but it is
not necessary.

To record the three cat facts above, I need some more references:
- My cat Hope needs a reference too, so she can be
  `http://pivotlabs.vc/animal/hope`.
- The concept of cat needs a reference as it is a 'type' of animal.
  `http://pivotlabs.vc/type/cat`.

I'm using a bit of structure in my URLs to help me organise them, but
this is not required - they just need to be unique.  But it helps everyone
trying to manage the data if order is introduced.

## Predicate references

The predicate part of a triple is also an entity, so it should be
referenced as a triple.  The concept of 'lives with' can have a URL of
`http://pivotlabs.vc/property/lives-with`.

The concept of 'has legs' needs a reference also, so it can have
a URL of `http://pivotlabs.vc/property/has-legs`.

## References and literals

References are always URLs.  There is another form of data in the graph:
the literal.  This is used for strings and numbers.  When describing that
Fred has 4 legs, the number 4 is going to appear in a statement as a literal.

As we said, triples are three parts:
- The subject is always a URL.
- The predicate is always a URL.
- The object can be a URL or a literal.

## Some triples

So, consolidating this, our 3 facts look like this:

| Subject                           | Predicate                                 | Object                            |
| --------------------------------- | ----------------------------------------- | --------------------------------- |
| `http://pivotlabs.vc/animal/fred` | `http://pivotlabs.vc/property/lives-with` | `http://pivotlabs.vc/animal/hope` |
| `http://pivotlabs.vc/animal/fred` | ???                                       | `http://pivotlabs.vc/type/cat`    |
| `http://pivotlabs.vc/animal/fred` | `http://pivotlabs.vc/property/has-legs`   | 4                                 |

There's a predicate we didn't define, and that's "is a".  As in the
fact "Fred is a cat".  It links an entity to its type.
As that's such a fundamental concept in RDF, there's
an existing predicate defined by the W3C in the RDF standard, which is
`http://www.w3.org/1999/02/22-rdf-syntax-ns#type`.

| Subject                         | Predicate                                       | Object                          |
| ------------------------------- | ----------------------------------------------- | ------------------------------- |
| `http://pivotlabs.vc/animal/fred` | `http://pivotlabs.vc/property/lives-with`         | `http://pivotlabs.vc/animal/hope` |
| `http://pivotlabs.vc/animal/fred` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | `http://pivotlabs.vc/type/cat`    |
| `http://pivotlabs.vc/animal/fred` | `http://pivotlabs.vc/property/has-legs`           | `4                               |

## The prefix

Before going any further, the syntax is starting to get a
little verbose and repetitive.  So, prefixes are used to replace long
repeated part of the URL. e.g.

| Prefix   | URL part                                      |
| -------- | --------------------------------------------- |
| `animal` | `http://pivotlabs.vc.animal/`                 |
| `rdf`    | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` |
| `prop`   | `http://pivotlabs.vc/property/`               |
| `type`   | `http://pivotlabs.vc/type/`                    |

Using the prefixes, our fact table looks like this:

| Subject       | Predicate         | Object        |
| ------------- | ----------------- | ------------- |
| `animal:fred` | `prop:lives-with` | `animal:hope` |
| `animal:fred` | `rdf:type`        | `type:cat`    |
| `animal:fred` | `prop:has-legs`   | `4`           |

This is a much more compact and readable representation of the data.

Prefixes are just a short-hand, `animal:fred` and
`http://pivotlabs.vc.animal/fred` mean the same thing.

## Defining types

We already included some entities which aren't completely defined
e.g. `prop:has-legs`.  This has meaning but our graph doesn't explain
that meaning.  In classic database design this would mean defining a
schema.  In knowledge graphs, that 'schema' information can just go in the
graph using RDF Schema standard.  The `rdf:type` predicate has already been
introduced.  For entities that are predicates or types, they can be
associated with RDF Schema entities to specify that they are
classes or properties.  Now we need a new prefix:

| Prefix    | URL part                                   |
| --------- | ------------------------------------------ |
| `rdfs`    | `http://www.w3.org/2000/01/rdf-schema#`    |

The entities `rdfs:Class` and `rdfs:Property` are used for types and predicates
respectively.  So now we have:

| Subject           | Predicate         | Object          |
| ----------------- | ----------------- | --------------- |
| `prop:lives-with` | `rdf:type`        | `rdfs:Property` |
| `prop:has-legs`   | `rdf:type`        | `rdfs:Property` |
| `type:cat`        | `rdf:type`        | `rdfs:Class`    |

Types can point to other derived types.  So, if it was of interest,
the types around the `type:cat` object could be elaborated.  A
`type:cat` could be a type of `type:mammal`, a `type:mammal` a type of
`type:animal`, and `type:animal` of type `rdfs:Class`.  For this
dataset, I'm not particularly interested in animal classification, so
will skip that complexity.

## Labels

The `rdfs:label` predicate is used to associate labels with any entity.
That includes entities, predicates and types we have defined.

| Subject              | Predicate         | Object          |
| -------------------- | ----------------- | --------------- |
| `type:cat`           | `rdfs:label`      | cat             |
| `animal:fred`        | `rdfs:label`      | Fred            |
| `animal:hope`        | `rdfs:label`      | Hope            |
| `prop:lives-with`    | `rdfs:label`      | lives with      |
| `prop:has-legs`      | `rdfs:label`      | has legs        |

## Other useful predicates

There are two other useful predicates which will be introduced now:
- `http://dbpedia.org/ontology/thumbnail` links an entity to a visual
  small thumbnail image. The object should be the URL of an image.
- `http://purl.org/dc/elements/1.1/relation` links an entity to a web
  page or further information.  The object should be a URL.

## Putting it all together

| Subject              | Predicate         | Object          |
| -------------------- | ----------------- | --------------- |
| `animal:fred`        | `rdfs:label`      | Fred            |
| `animal:fred`        | `rdf:type`        | `type:cat`      |
| `animal:fred`        | `prop:lives-with` | `animal:hope`   |
| `animal:fred`        | `prop:has-legs`   | `4`             |
| `animal:hope`        | `rdfs:label`      | Hope            |
| `animal:hope`        | `rdf:type`        | `type:cat`      |
| `animal:hope`        | `prop:lives-with` | `animal:fred`   |
| `animal:hope`        | `prop:has-legs`   | `4`             |
| `prop:lives-with`    | `rdf:type`        | `rdfs:Property` |
| `prop:lives-with`    | `rdfs:label`      | lives with      |
| `prop:has-legs`      | `rdf:type`        | `rdfs:Property` |
| `prop:has-legs`      | `rdfs:label`      | has legs        |
| `type:cat`           | `rdf:type`        | `rdfs:Class`    |
| `type:cat`           | `rdfs:label`      | cat             |

## N-Triples

The simplest file format for RDF triples is N-Triples.  Each line of the
file describes a triple.  The S, P, O elements are written out, space-separated.
Each element is surrounded either by angle-brackets for a URI, or double-quotes
for literals.  Here's a snippet:

```
<http://pivotlabs.vc.animal/fred> <http://pivotlabs.vc/property/has-legs> "4"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://pivotlabs.vc.animal/fred> <http://pivotlabs.vc/property/lives-with> <http://pivotlabs.vc.animal/hope> .
<http://pivotlabs.vc.animal/fred> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://pivotlabs.vc/type/cat> .
<http://pivotlabs.vc.animal/fred> <http://www.w3.org/2000/01/rdf-schema#label> "Fred" .
<http://pivotlabs.vc.animal/hope> <http://pivotlabs.vc/property/has-legs> "4"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://pivotlabs.vc.animal/hope> <http://pivotlabs.vc/property/lives-with> <http://pivotlabs.vc.animal/fred> .
<http://pivotlabs.vc.animal/hope> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://pivotlabs.vc/type/cat> .
<http://pivotlabs.vc.animal/hope> <http://www.w3.org/2000/01/rdf-schema#label> "Hope" .
<http://pivotlabs.vc/property/has-legs> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Property> .
<http://pivotlabs.vc/property/has-legs> <http://www.w3.org/2000/01/rdf-schema#label> "has legs" .
<http://pivotlabs.vc/property/lives-with> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Property> .
<http://pivotlabs.vc/property/lives-with> <http://www.w3.org/2000/01/rdf-schema#label> "lives with" .
<http://pivotlabs.vc/type/cat> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
<http://pivotlabs.vc/type/cat> <http://www.w3.org/2000/01/rdf-schema#label> "cat" .
```

## Turtle

N-Triples are very verbose, and not so easy to edit.  There's a lot
of repitition.  Another format is Turtle format.  Turtle allows prefixes to
be defined and used.  The format also allows grouping so that the
entity strings don't need to be repeated.

```
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix animal: <http://pivotlabs.vc/animal/> .
@prefix prop: <http://pivotlabs.vc/property/> .
@prefix type: <http://pivotlabs.vc/type/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

animal:fred
    prop:has-legs 4 ;
    prop:lives-with animal:hope ;
    a type:cat ;
    rdfs:label "Fred" .

animal:hope
    prop:has-legs 4 ;
    prop:lives-with animal:fred ;
    a type:cat ;
    rdfs:label "Hope" .

prop:has-legs
    a rdfs:Property ;
    rdfs:label "has legs" .

prop:lives-with
    a rdfs:Property ;
    rdfs:label "lives with" .

type:cat
    a rdfs:Class ;
    rdfs:label "cat" .
```

## Going further

The RDF technologies and standards are big and very powerful for knowledge
management, and we only scraped the surface here.  But this is enough to
get started with our knowledge graph.

