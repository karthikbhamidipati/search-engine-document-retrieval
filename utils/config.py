import os


class Config:
    """ Class to define the configurations
    """

    # common
    LOCAL_HOST = os.environ.get('LOCAL_HOST') or "127.0.0.1"

    # elasticsearch configurations
    ELASTIC_SEARCH_PORT = os.environ.get('ELASTIC_SEARCH_PORT') or "9200"
    ELASTIC_SEARCH_URI = os.environ.get('ELASTIC_SEARCH_URI') or ":".join((LOCAL_HOST, ELASTIC_SEARCH_PORT))
    ELASTIC_SEARCH_MAX_THREADS = os.environ.get('ELASTIC_SEARCH_MAX_THREADS') or 10

    # subsampling configurations
    USE_CLUSTERS = os.environ.get('USE_CLUSTERS') or False
    SUBSAMPLED_ROOT = os.environ.get('SUBSAMPLED_ROOT') or "data/"
    NUM_SAMPLES = os.environ.get('NUM_SAMPLES') or 150
    NUM_DOCS_PER_QUERY = os.environ.get('NUM_DOCS_PER_QUERY') or 20
    CLUSTER_IDS = (0, 3, 4, 5, 6)

    # input files
    DOCS_FILE_NAME = os.environ.get('file_name') or "msmarco-docs.tsv"
    QUERIES_FILE_NAME = os.environ.get('QUERIES_FILE_NAME') or "msmarco-doctrain-queries.tsv"
    TOP100_FILE_NAME = os.environ.get('TOP100_FILE_NAME') or "msmarco-doctrain-top100"
    CLUSTERED_QUERIES_FILE_NAME = os.environ.get('CLUSTERED_QUERIES_FILE_NAME') or "msmarco-clustered-queries.csv"

    # sampled files
    DOCS_FILE_SAMPLED = os.path.splitext(DOCS_FILE_NAME)[0] + ".csv"
    QUERIES_FILE_SAMPLED = os.path.splitext(QUERIES_FILE_NAME)[0] + ".csv"
    TOP100_FILE_SAMPLED = os.path.splitext(TOP100_FILE_NAME)[0] + ".csv"

    # data headers
    DOCS_HEADERS = ['docid', 'url', 'title', 'body']
    QUERIES_HEADERS = ['qid', 'query']
    TOP100_HEADERS = ['qid', 'Q0', 'docid', 'rank', 'score', 'runstring']
    CLUSTERED_QUERIES_HEADERS = ['qid', 'query', 'cluster']

    # data keys
    DOCID_KEY = "docid"
    QUERYID_KEY = "qid"

    # indices
    VSM_INDEX_KEY = "msmarco_docs_vsm"
    BM25_INDEX_KEY = "msmarco_docs_bm25"

    # webapp
    NUM_RECORDS_TO_RETRIEVE = NUM_DOCS_PER_QUERY
    APP_PORT = os.environ.get('APP_PORT') or "5000"
    APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY') or 'mysecret'

    # warnings
    FILTER_WARNINGS = True


config = Config()


class Mappings:
    """ Class to define mappings
    """

    # Vector space model using tf-idf similarity
    VSM_MAPPING = {
        "settings": {
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 15
                    }
                },
                "analyzer": {
                    "text_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stemmer", "stop"]
                    },
                    "autocomplete": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                    }
                }
            },
            "index": {
                "similarity": {
                    "scripted_tfidf": {
                        "type": "scripted",
                        "weight_script": {
                            "source": """
                                        double idf = Math.log((field.docCount + 1.0) / (term.docFreq + 1.0)) + 1.0; 
                                        return query.boost * idf;
                                      """
                        },
                        "script": {
                            "source": """
                                        double tf = Math.sqrt(doc.freq); 
                                        double norm = 1 / Math.sqrt(doc.length); 
                                        return weight * tf * norm;
                                      """
                        }
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "docid": {"type": "keyword"},
                "url": {"type": "keyword"},
                "query": {"type": "text", "analyzer": "autocomplete"},
                "title": {"type": "text", "analyzer": "text_analyzer", "similarity": "scripted_tfidf"},
                "body": {"type": "text", "analyzer": "text_analyzer", "similarity": "scripted_tfidf"}
            }
        }
    }

    # BM25 model mapping
    BM25_MAPPING = {
        "settings": {
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 15
                    }
                },
                "analyzer": {
                    "text_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stemmer", "stop"]
                    },
                    "autocomplete": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                    }
                }
            },
            "index": {
                "similarity": {
                    "bm25": {
                        "type": "BM25",
                        "b": 0.75,
                        "k1": 1.2
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "docid": {"type": "keyword"},
                "url": {"type": "keyword"},
                "query": {"type": "text", "analyzer": "autocomplete"},
                "title": {"type": "text", "analyzer": "text_analyzer", "similarity": "bm25"},
                "body": {"type": "text", "analyzer": "text_analyzer", "similarity": "bm25"}
            }
        }
    }

    # Metrics
    DCG_METRIC = {
        "name": "Discounted cumulative gain",
        "query": {
            "dcg": {
                "k": Config.NUM_DOCS_PER_QUERY,
                "normalize": "true"
            }
        }
    }

    PRECISION_METRIC = {
        "name": "Precision at {}".format(Config.NUM_DOCS_PER_QUERY),
        "query": {
            "precision": {
                "k": Config.NUM_DOCS_PER_QUERY,
                "relevant_rating_threshold": 1,
                "ignore_unlabeled": "false"
            }
        }
    }

    RECALL_METRIC = {
        "name": "Recall at {}".format(Config.NUM_DOCS_PER_QUERY),
        "query": {
            "recall": {
                "k": Config.NUM_DOCS_PER_QUERY,
                "relevant_rating_threshold": 1
            }
        }
    }

    MRR_METRIC = {
        "name": "Mean reciprocal rank",
        "query": {
            "mean_reciprocal_rank": {
                "k": Config.NUM_DOCS_PER_QUERY,
                "relevant_rating_threshold": 1
            }
        }
    }

    ERR_METRIC = {
        "name": "Expected reciprocal rank",
        "query": {
            "expected_reciprocal_rank": {
                "maximum_relevance": 3,
                "k": Config.NUM_DOCS_PER_QUERY
            }
        }
    }


mappings = Mappings()
