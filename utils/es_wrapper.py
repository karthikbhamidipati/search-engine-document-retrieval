import requests
from elasticsearch import Elasticsearch

from config import config


class ElasticWrapper:
    """ TODO add documentation, logging, error handling
    """

    def __init__(self, uri=config.ELASTIC_SEARCH_URI):
        self._establish_connection(uri)

    def create_index(self, index, body=None, recreate_exist=False):
        if recreate_exist:
            self.drop_index(index)

        if not self.elastic_client.indices.exists(index):
            self.elastic_client.indices.create(index, body=body)
        else:
            print('Index already exists: %s, pass recreate_exist=True '
                  'to delete and create the index' % index)

    def drop_index(self, index):
        self.elastic_client.indices.delete(index, ignore=[400, 404])

    def bulk_index(self, index, body):
        try:
            response = self.elastic_client.bulk(index=index, body=body)
            print('RESPONSE for document {} : {}\n'.format(index, response))
        except Exception as e:
            print('ERROR for document {} : {}\n'.format(index, e))

    def search_index(self, index, query, size=config.NUM_RECORDS_TO_RETRIEVE):
        return self.elastic_client.search(index=index, body=query, size=size)

    def get_index(self, index, id):
        return self.elastic_client.get(index=index, id=id)

    def _establish_connection(self, uri):
        if requests.get(uri).ok:
            self.elastic_client = Elasticsearch([uri], maxsize=config.MAX_RECORDS_TO_RETRIEVE)
        else:
            raise ValueError("Invalid URI: %s" % uri)

    def close(self):
        self.elastic_client.close()