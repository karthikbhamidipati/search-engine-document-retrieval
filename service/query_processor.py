import os

import pandas as pd

from utils.config import config, mappings
from utils.es_wrapper import ElasticWrapper


def get_docs_json(index, docs_df):
    for _, row in docs_df.iterrows():
        yield {
            "_index": index,
            "_id": row[config.DOCID_KEY],
            "_source": {
                config.DOCID_KEY: row[config.DOCID_KEY],
                "url": row["url"],
                "title": row["title"],
                "body": row["body"]
            }
        }


def bulk_index_docs(es_wrapper, docs_df, index, mapping):
    es_wrapper.create_index(index, mapping, recreate_exist=True)
    es_wrapper.bulk_index(index, get_docs_json(index, docs_df))


def index_docs(doc_path=None):
    if not doc_path:
        doc_path = os.path.join(config.SUBSAMPLED_ROOT, config.DOCS_FILE_NAME)
    docs_df = pd.read_csv(doc_path)

    es_wrapper = ElasticWrapper()
    bulk_index_docs(es_wrapper, docs_df, config.VSM_INDEX_KEY, mappings.VSM_MAPPING)
    bulk_index_docs(es_wrapper, docs_df, config.BM25_INDEX_KEY, mappings.BM25_MAPPING)
    es_wrapper.close()