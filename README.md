
# UK Innovation Graph Community Project

## Summary

This project curates a data set describing information about the UK
innovation ecosystem.  The information is available to explore using
a simple graph viewer application.
This is currently hosted at the pivotlabs.vc site.  A good starting
point is this URL:

https://graph.innovate.pivotlabs.vc/graph?node=http:%2F%2Fpivotlabs.vc%2Fchallenges%2Fs%2Fktn.

The dataset is also available through an open graph API supporting the
SPARQL query language allowing access to the underlying dataset.

## Data curation

The source data is stored directly in this Github repository, and assembled
into a graph which is then bundled with the software repositories and
released to the cloud.

## Data structures

Data sets are stored in subdirectories of the `data` directory.

There are currently two data sets:
- `organisations`: This records the name, title and description of UK
  organisations which sponsor innovation challenges.
- `uk-innovation-challenges`: Details of innovation challenges sponsored by
  UK organisations.  This includes descriptions, sponsoring organisations,
  open/close dates, and topics derived from naive topic extraction.

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

## Schema

TBD

## Community Contributions

Community contributions to this data set are welcome and encouraged.
To contribute, clone this Github repository, fork the repository and
make a pull-request, which we will review.

Your pull request will trigger a Github action which runs a data load
which provides a simple verification check that your change hasn't
broken anything.  We'll take the discussion on your pull request if
there's anything to discuss.

Your pull request can propose a change to an existing data set, or you
can add a new data set by creating a subdirectory below the data
directory.

The curation process can accept new data processing types if needed.



