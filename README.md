
# UK Innovation Graph Community Project

## Summary

This project curates a data set describing information about the UK
innovation ecosystem.  The information is available to explore using
a simple graph viewer application.
This is currently hosted at the pivotlabs.vc site.  A good starting
point is this URL:

https://graph.innovate.pivotlabs.vc/graph?node=http:%2F%2Fpivotlabs.vc%2Finnov%2Forganisation%2Fktn

The dataset is also available through an open graph API supporting the
SPARQL query language allowing access to the underlying dataset.

The purpose of publishing this project is to invite the whole community to
engage and help grow the dataset.  This Github repository is set up with
Github actions to automatically deploy changes.  See below.
Everyone is encouraged to contribute, add datasets, and grow and extend
the schema to meet the community's needs.

## Data curation

The source data is stored directly in this Github repository, and assembled
into a graph which is then bundled with the software repositories and
released to the cloud.

For existing data sets see [Datasets](docs/README.datasets.md).

To learn more about data curation and how to add data see:

See [Data curation](docs/README.curation.md).

## Schema

See [Crash course in knowledge graph concepts](docs/README.knowledge-graphs.md).

See [Schema](docs/README.schema.md).

The schema lives in the `schema/schema.ttl` file, and is in Turtle format.

Data is validated against the schema in Github action pipelines, and a failure
is flagged in the pull request or deploy pipelines as a failure.

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

If you want to know more or need more documentation, raise an issue.
If you want collaboration access, raise an issue.

There are three deployments.  The deployment from Github is automated,
deployed environments track the branches described below.  People who wish
to collaborate will be granted access to deploy to merge to dev to test their
own changes.

| Environment  | Branch    | Application URL                     |
| ------------ | --------- | ----------------------------------- |
| Development  | dev       | https://graph.dev.pivotlabs.vc      |
| Staging      | staging   | https://graph.staging.pivotlabs.vc  |
| Production   | master    | https://graph.innovate.pivotlabs.vc |

## Licence

This is released under the Apache 2 licence.  You are free to contribute
and copy the code or host this yourself under the terms of the
[LICENCE](LICENCE).


