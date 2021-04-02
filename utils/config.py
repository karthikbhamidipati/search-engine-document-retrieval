import os


class Config:
    # common
    LOCAL_HOST = os.environ.get('LOCAL_HOST') or "127.0.0.1"

    # elasticsearch configurations
    ELASTIC_SEARCH_PORT = os.environ.get('ELASTIC_SEARCH_PORT') or "9200"
    ELASTIC_SEARCH_URI = os.environ.get('ELASTIC_SEARCH_URI') or ":".join((LOCAL_HOST, ELASTIC_SEARCH_PORT))
    ELASTIC_SEARCH_MAX_THREADS = os.environ.get('ELASTIC_SEARCH_MAX_THREADS') or 10

    # subsampling configurations
    SUBSAMPLED_ROOT = os.environ.get('SUBSAMPLED_ROOT') or "data/"
    NUM_SAMPLES = os.environ.get('NUM_SAMPLES') or 1500

    # input data configurations
    DOCS_FILE_NAME = os.environ.get('file_name') or "msmarco-docs.tsv"
    QUERIES_FILE_NAME = os.environ.get('QUERIES_FILE_NAME') or "msmarco-doctrain-queries.tsv"
    TOP100_FILE_NAME = os.environ.get('TOP100_FILE_NAME') or "msmarco-doctrain-top100"

    DOCS_HEADERS = ['docid', 'url', 'title', 'body']
    QUERIES_HEADERS = ['qid', 'query']
    TOP100_HEADERS = ['qid', 'Q0', 'docid', 'rank', 'score', 'runstring']

    DOCID_KEY = "docid"
    QUERYID_KEY = "qid"

    # indices
    VSM_INDEX_KEY = "msmarco_docs_vsm"
    BM25_INDEX_KEY = "msmarco_docs_bm25"

    # webapp
    NUM_RECORDS_TO_RETRIEVE = 10
    APP_PORT = os.environ.get('APP_PORT') or "5000"
    APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY') or 'mysecret'


config = Config()


class Mappings:
    """ Class to define mappings
    """

    # TF-IDF with cosine similarity using vector space model
    VSM_MAPPING = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stemmer", "stop"]
                    }
                }
            },
            "index": {
                "similarity": {
                    "scripted_tfidf": {
                        "type": "scripted",
                        "script": {
                            "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
                        }
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "docid": {"type": "keyword"},
                "url": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "my_analyzer", "similarity": "scripted_tfidf"},
                "body": {"type": "text", "analyzer": "my_analyzer", "similarity": "scripted_tfidf"}
            }
        }
    }

    # BM25 model mapping
    BM25_MAPPING = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stemmer", "stop"]
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
                "title": {"type": "text", "analyzer": "my_analyzer", "similarity": "bm25"},
                "body": {"type": "text", "analyzer": "my_analyzer", "similarity": "bm25"}
            }
        }
    }


mappings = Mappings()
