from elasticsearch import Elasticsearch, helpers

from utils.config import Config


class ElasticWrapper:

    def __init__(self, uri=Config.ELASTIC_SEARCH_URI):
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
            response = helpers.bulk(self.elastic_client, body)
            print('RESPONSE for index {} : {}\n'.format(index, response))
        except Exception as e:
            print('ERROR for index {} : {}\n'.format(index, e))

    def search_index(self, index, query, size=Config.NUM_RECORDS_TO_RETRIEVE):
        return self.elastic_client.search(index=index, body=query, size=size)

    def get_index(self, index, id):
        return self.elastic_client.get(index=index, id=id)

    def rank_eval(self, index, body):
        return self.elastic_client.rank_eval(index=index, body=body)

    def _establish_connection(self, uri):
        try:
            self.elastic_client = Elasticsearch([uri], maxsize=Config.ELASTIC_SEARCH_MAX_THREADS)
        except Exception as e:
            raise ValueError("Invalid URI: %s \nError: %s" % uri, e)

    def close(self):
        self.elastic_client.close()
