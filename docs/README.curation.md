
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
- `processing`: describes how the data is parsed and loaded.

## The `csv` processing type

This is for CSV files.  The metadata file should also contain:
- `input`: the filename of the CSV input data
- `fields`: a list of types for the columns of the CSV file.  The number
  of field list entries must equal the number of columns in the CSV file.
- `id-prefix`: a prefix added to the identifier column entries to form
  unique identifiers.

The first field type must be `%%identity%%` which indicates that the
first column is used as the identifier of an object.  The object identifier
is added to the end of the `id-prefix` string, and an identifier
results.

The identifier should be a unique ID across all the data, and needs
to have a http:// or https:// prefix.  Although that makes it look like
a URL, it doesn't actually need to exist as a web page on the real internet.
To make the URL unique you can make up something random or put your
organisation's web site in it.

## The `turtle` processing type

This is for Turtle data files which are already constructed in accordance
with the schema.

The metadata file should also contain:
- `input`: the filename of the CSV input data
