import os

import dask.dataframe as dd

from utils.config import Config, mappings
from utils.es_wrapper import ElasticWrapper


def get_docs_json(index, docs_df):
    for _, row in docs_df.iterrows():
        yield {
            "_index": index,
            "_id": row[Config.DOCID_KEY],
            "_source": {
                Config.DOCID_KEY: row[Config.DOCID_KEY],
                "url": row["url"],
                "query": row["title"],
                "title": row["title"],
                "body": row["body"]
            }
        }


def bulk_index_docs(es_wrapper, docs_df, index, mapping):
    es_wrapper.create_index(index, mapping, recreate_exist=True)
    es_wrapper.bulk_index(index, get_docs_json(index, docs_df))


def index_docs(doc_path=None):
    if not doc_path:
        doc_path = os.path.join(Config.SUBSAMPLED_ROOT, Config.DOCS_FILE_SAMPLED)
    docs_df = dd.read_csv(doc_path, keep_default_na=False)

    es_wrapper = ElasticWrapper()
    bulk_index_docs(es_wrapper, docs_df, Config.VSM_INDEX_KEY, mappings.VSM_MAPPING)
    bulk_index_docs(es_wrapper, docs_df, Config.BM25_INDEX_KEY, mappings.BM25_MAPPING)
    es_wrapper.close()