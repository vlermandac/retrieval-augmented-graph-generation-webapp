from header import *


class TestRAG(unittest.TestCase):
    def setUp(self, root=ROOT):
        self.vars = ConfigVariables(root)
        env_var = self.vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD',
                                'CA_CERT', 'OPENAI_API_KEY')
        cert_mod = root + env_var['CA_CERT']
        env_var['CA_CERT'] = cert_mod
        self.clients = Clients(**env_var)

        self.rag = RAG(self.clients, 'goodfellas-chunk', # CAMBIAR GOODFELLAS
                       **self.vars('embedding_model', 'dims', 'llm', 'k'))

    def test_generation(self):
        print(self.vars('embedding_model', 'dims', 'llm', 'k'))
        response = self.rag(query="What is the movie Goodfellas about?")
        self.assertTrue(response)
        print("Contextualized query:")
        print(self.rag.prompt)
        print("\nResponse:")
        print(response)
        print("\nResult IDs:")
        print(self.rag.get_result_ids())


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
