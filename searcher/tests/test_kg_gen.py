from header import *
from kg import KnowledgeGraphConstructor


class TestKG(unittest.TestCase):
    def setUp(self, root=ROOT):
        self.vars = ConfigVariables(root)
        env_var = self.vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD',
                                'CA_CERT', 'OPENAI_API_KEY')
        cert_mod = root + env_var['CA_CERT']
        env_var['CA_CERT'] = cert_mod
        self.clients = Clients(**env_var)

        self.kg = KnowledgeGraphConstructor()

    def test_chunks_to_triplet(self):
        chunks = self.kg.data_from_es(self.clients.elastic_search(), 'goodfellas-chunk', 30)
        triplets = self.kg.chunk_to_triplets(self.clients.open_ai(), 'gpt-3.5-turbo', chunks)
        self.kg.process_triplets(triplets)
        with open('graph-data.json', 'w') as f:
            f.write(self.kg.serialize())


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
