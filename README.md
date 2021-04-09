# search-engine-document-retrieval

## Overview

Implementation of a search engine with two different retrieval models, evaluation of the models’ results using the queries and their top-100 relevant docs from the MS MARCO dataset and a web interface for the user to query the data and retrieve results.

Retrieval Models implemented:

1. VSM
2. BM25

## Requirements

Unzip the folder, `cd` onto the project directory and run ```pip install -r requirements.txt``` from terminal to install the required dependencies.

* `elasticsearch-python` version should be 7.12.0 or above
* `flask` version should be 1.1.2 or above
* `pandas` version should be 1.2.3 or above
* `dask[dataframe]`

## Execution

* Before execution of the following scripts, Elasticsearch should be up and runnning in the localhost port number 9200.
* Run ```python main.py index``` file to run the indexing of the documents on elasticsearch.
* Run ```python main.py eval``` file to to run evaluation of top 100 queries.
* Run ```python main.py start_app```file to start the front-end part of the search engine. Search engine's webpage can be reached via http://localhost:5000/
