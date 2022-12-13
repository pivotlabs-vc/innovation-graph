
# Curation

## Overview

If you want to add data which conforms to existing schema, you need
to create a new sub-directory under `data`, and add your data file
and a `metadata.json` file.

If you data needs schema modifications, you will also need to change
the [Schema](README.schema.md).

## Datasets

Data sets are stored in subdirectories of the `data` directory.

We envisage more data sets added over time.  Each data set has a
`metadata.json` file in JSON format describing the dataset.
The file must contain the following fields:
- `id`: A unique ID for the dataset.
- `description`: Human-readable description.
- `contributors`: A list of names / emails / identifiers by which the
  contributors to the dataset want to be known.
- `origin`: Human-readable explanation of the source of the dataset.
- `copyright`: A human-readable copyright claim.  Pull requests for
  datasets which aren't compatible with this repositories licence can't be
  accepted, although we can discuss other ways of contributing.
- `processing`: describes how the data is parsed and loaded, this can be
  `csv` or `turtle`.

## The `csv` processing type

This is for CSV files.  The metadata file should also contain:
- `input`: the filename of the CSV input data
- A list of the fields in the CSV file.  Either set
  `fields` to be a list of names, one for each column, or set
  `fields-from-header` to indicate that the fields list can be loaded
  from the first line of the CSV file.  The field names aren't
  particularly important, they are referenced elsewhere in the configuration
  file.
- An optional `skip` field set to an integer, indicating how many rows
  of the CSV file to skip.
- An `object` field describing how a row from the CSV file is handled:
  - The `class` field should specify the RDF type of the primary object
    created for each row.
  - The `id-field` field specifies which CSV column contains a unique
    identifier for each row.  This should be a name from the field list.
  - The optional `id-prefix` specifies a string prepended to the value
    from the `id-field` field to construct a unique ID before RDF
    processing.  This should begin with a prefix.
  - The `properties` field is a list, one object for each CSV column
    (but not the ID column).  Each element consists of:
    - `predicate` specifies the RDF predicate for this CSV column
    - `object-field` refers to the CSV `field` list identifying the column
      to work with.
    - An optional `ignore` field which contains an object.  If a value
      in the CSV column matches a key in the object, and the matching
      value is set to true, the value will be skipped.
    - An optional `map` field.  If values match the key in the object,
      they are mapped to the value.
    - For a literal, the optional `datatype` field specifies the XSD
      datatype to apply to the value.  Uuseful types are: `xsd:integer`,
      `xsd:decimal`, `xsd:date`for YYYY-MM-DD format dates.  If not
      specified, a string type is used.
    - To create a class object from a CSV column:
      - Add an `object-type` field containing the RDF type including a
        prefix.
      - Specify `derive-object-id` or `use-object-id-hash`.

FIXME: This documentation is very difficult to follow.  Needs a HOWTO
approach.

The identifier should be a unique ID across all the data, and needs
to have a http:// or https:// prefix.  Although that makes it look like
a URL, it doesn't actually need to exist as a web page on the real internet.
To make the URL unique you can make up something random or put your
organisation's web site in it.

As the graph is an RDF graph, the literal values have a type defined
by the XSD standard.  The default type is string or `xsd:string`.

You can map a field to a different type mapping with the
optional`datatypes` field e.g.
To set `property:founded` to be a year, we map `property:founded` to
`xsd:gYear`.

```
    "fields": [
        ...
	"property:founded",
	...
    ],
    "datatypes": {
	"property:founded": "xsd:gYear"
    },
```

Other useful types are: `xsd:integer`, `xsd:decimal`, `xsd:date`
for YYYY-MM-DD format dates.

## The `turtle` processing type

This is for Turtle data files which are already constructed in accordance
with the schema.

The metadata file should also contain:
- `input`: the filename of the CSV input data

