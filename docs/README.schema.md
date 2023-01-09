
# Schema

The knowledge graph is built on RDF technology, and makes use of
RDF constructs to define schema.

## Innovation challenge

This schema was created for this project and is defined
[here](../schema/challenge.ttl).

- Type: `http://pivotlabs.vc/innov/t/challenge`
- Abbreviation: `type:challenge`

Properties:
- `http://pivotlabs.vc/innov/t/challenge#opens`: Date innovation challenge
  opens
- `http://pivotlabs.vc/innov/t/challenge#closes`: Date innovation challenge
  closes
- `http://pivotlabs.vc/innov/t/challenge#has-topic`: links to topic entity
- `http://pivotlabs.vc/innov/t/challenge#title`: Innovation challenge title
- `http://pivotlabs.vc/innov/t/challenge#has-sponsor`: links to innovation
  challenge sponsoring organisation.
- `http://pivotlabs.vc/innov/t/challenge#description`: Innovation challenge
  long textual description

## Schema.org

This project imports schema.org's full schema
[here](../schema/schemaorg-current-https.ttl).  The released schema
appears to be inconsistent, so we replace `rdf:Property` with
`rdfs:Property` to make it consistent with the RDF Schema specification.

A number of fundamental entities used by `schema.org` are defined
[here](../schema/schemaorg.ttl).

### Organisation

Defined by [Schema.org](https://schema.org/Organization).

- Type: `https://schema.org/Organization`
- Abbreviation: `schema:Organization`

Several types of government department have been created by this project
which are sub-classes of the Organization type defined
[here](../schema/organisation.ttl).

Watch out for UK vs US spelling, `schema.org` uses `Organization`.

### Innovation challenge topic

This project uses `DefinedTerm`
from [Schema.org](https://schema.org/DefinedTerm).

- Type: `https://schema.org/DefinedTerm`
- Abbreviation: `schema:DefinedTerm`

### Person

This project uses `Person` from [Schema.org](https://schema.org/DefinedTerm).

- Type: `https://schema.org/Person`
- Abbreviation: `schema:Person`

### Occupation

This project uses `Occupation` from
[Schema.org](https://schema.org/Occupation).

- Type: `https://schema.org/Occupation`
- Abbreviation: `schema:Occupation`

