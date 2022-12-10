
# Crash course in knowledge graph concepts

## Facts

The knowledge graph represents a collection of assertions of facts.
Starting with a collection of facts about my cats:

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
Fred has 4 legs, the number 4 is going to appear in a statement as a triple.

As we said, triples are three parts:
- The subject is always a URL.
- The predicate is always a URL.
- The object can be a URL or a literal.

## Some triples

So, consolidating this, our 3 facts look like this:

| Subject                         | Predicate                               | Object                          |
| ------------------------------- | --------------------------------------- | ------------------------------- |
| http://pivotlabs.vc/animal/fred | http://pivotlabs.vc/property/lives-with | http://pivotlabs.vc/animal/hope |
| http://pivotlabs.vc/animal/fred | ???                                     | http://pivotlabs.vc/type/cat    |
| http://pivotlabs.vc/animal/fred | http://pivotlabs.vc/property/has-legs   | 4                               |

There's a predicate we didn't define, and that's "is a".  As in the
fact "Fred is a cat".  As that's such a fundamental in RDF, there's
an existing predicate defined by the W3C in the RDF standard, which is
`http://www.w3.org/1999/02/22-rdf-syntax-ns#type`.

| Subject                         | Predicate                                       | Object                          |
| ------------------------------- | ----------------------------------------------- | ------------------------------- |
| http://pivotlabs.vc/animal/fred | http://pivotlabs.vc/property/lives-with         | http://pivotlabs.vc/animal/hope |
| http://pivotlabs.vc/animal/fred | http://www.w3.org/1999/02/22-rdf-syntax-ns#type | http://pivotlabs.vc/type/cat    |
| http://pivotlabs.vc/animal/fred | http://pivotlabs.vc/property/has-legs           | 4                               |

## The prefix

Before going any further, the syntax is starting to get a
little verbose and repetitive.  So, prefixes are used to replace long
repeated part of the URL. e.g.

| Prefix               | URL part                                    |
| -------------------- | ------------------------------------------- |
| animal               | http://pivotlabs.vc.animal/                 |
| rdf                  | http://www.w3.org/1999/02/22-rdf-syntax-ns# |
| prop                 | http://pivotlabs.vc/property/               |
| type                 | http://pivotlabs.vc/type                    |

Using the prefixes, our fact table looks like this:

| Subject     | Predicate       | Object      |
| ----------- | --------------- | ----------- |
| animal:fred | prop:lives-with | animal:hope |
| animal:fred | rdf:type        | type:cat    |
| animal:fred | prop:has-legs   | 4           |

This is a much more compact and readable representation of the data.

