from header import *
from kg import KnowledgeGraphBuilder


class TestKG(unittest.TestCase):
    def setUp(self, root=ROOT):
        self.vars = ConfigVariables(root)
        env_var = self.vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD',
                                     'CA_CERT', 'OPENAI_API_KEY')
        cert_mod = root + env_var['CA_CERT']
        env_var['CA_CERT'] = cert_mod
        self.clients = Clients(**env_var)

        self.kg_builder = KnowledgeGraphBuilder()

    def test_chunks_to_triplet(self):
        # We assume that the elastic search index is already created
        chunks = self.clients.elastic_search().search(index='moby_dick-chunk', size=30)
        triplets = self.kg_builder.chunk_to_triplets(self.clients.open_ai(), 'gpt-4o', chunks) # probar
        self.kg_builder.process_triplets(triplets)
        print(self.kg_builder.serialize())
        with open('graph-data.json', 'w') as f:
            f.write(self.kg_builder.serialize())


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
