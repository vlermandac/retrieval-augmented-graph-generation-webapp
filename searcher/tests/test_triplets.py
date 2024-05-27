from header import *
from triplet import TripletBuilder


class TestTriplets(unittest.TestCase):
    def setUp(self, root=ROOT):
        self.vars = ConfigVariables(root)
        env_var = self.vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD',
                                     'CA_CERT', 'OPENAI_API_KEY')
        cert_mod = root + env_var['CA_CERT']
        env_var['CA_CERT'] = cert_mod
        self.clients = Clients(**env_var)

        self.kg_builder = TripletBuilder()

    def test_chunks_to_triplet(self):

        # We assume that the elastic search index is already created
        chunks = self.clients.elastic_search().search(index='goodfellas-chunk', size=5)
        triplets = self.kg_builder.chunk_to_triplets(self.clients.open_ai(), 'gpt-3.5-turbo', chunks)
        with open('../../triplets.json', 'w') as f:
            f.write(triplets.model_dump_json(indent=2))


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
