
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
- `copyright`: A human-readable copyright claim.
- `licence`: A URL to a human-readable licence.
- `processing`: describes how the data is parsed and loaded, this can be
  `csv` or `turtle`.

## The `csv` processing type

This is for CSV files.  Not currently documented, see examples in the
data directory, or raise an issue if you want help.

## The `turtle` processing type

This is for Turtle data files which are already constructed in accordance
with the schema.

The metadata file should also contain:
- `input`: the filename of the CSV input data

