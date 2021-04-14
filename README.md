# search-engine-document-retrieval

## Overview

Implementation of a search engine with two different retrieval models, evaluation of the models’ results using the queries and their top-100 relevant docs from the MS MARCO dataset and a web interface for the user to query the data and retrieve results. The data is available in `data` directory in the project root.

Retrieval Models implemented:

1. VSM
2. BM25

## Pre-requisites

- Unzip the folder, `cd` onto the project directory
- Start `elasticsearch` in localhost on port `9200`
- Run ```pip install -r requirements.txt``` from terminal to install the below required dependencies.
   * `elasticsearch-python` version should be 7.12.0 or above
   * `flask` version should be 1.1.2 or above
   * `pandas` version should be 1.2.3 or above
   * `dask[dataframe]`

## Execution

Before execution of the following scripts, please make sure to run the pre-requisites as mentioned above
* Run ```python main.py index``` file to run the indexing of the documents on elasticsearch.
* Run ```python main.py start_app```file to start the front-end part of the search engine. Search engine's webpage can be reached via http://localhost:5000/
* Run ```python main.py eval``` file to to run evaluation of top 100 queries.

## Contributors

- [Karthik Bhamidipati](https://github.com/vamshikarthik)
- [Omer Faruk Yildirim](https://github.com/farukyld)
- [Sudipta Mondal](https://github.com/sudiptamondal1802)
