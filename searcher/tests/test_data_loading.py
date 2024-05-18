from header import *


class TestDataLoading(unittest.TestCase):
    def setUp(self, root=ROOT):
        vars = ConfigVariables(root)
        env_var = vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD',
                                'CA_CERT', 'OPENAI_API_KEY')
        cert_mod = root + env_var['CA_CERT']
        env_var['CA_CERT'] = cert_mod
        self.clients = Clients(**env_var)

        self.dir_path = "files/"
        self.chunk_size = 20
        self.overlap = 1
        self.embedding_model = 'text-embedding-3-small'
        self.dims = 10
        self.chunks = data_loading.run(self.clients, self.dir_path, self.chunk_size,
                                      self.overlap, self.embedding_model, self.dims)[0]
        self.doc_name = self.chunks[0].metadata['document_name']

    def test_document(self):
        print(f"Document name: {self.doc_name}")
        response = \
            self.clients.elastic_search().search(index='document', id=str(self.doc_name))
        self.assertIsNotNone(response, "Document not found")

        print("Document info: ", response)
        self.clients.elastic_search().delete(index='document', id=self.doc_name)

        response = self.clients.elastic_search().delete(index=f"{self.doc_name}-chunk")
        print("Deleted chunks: ", response)

    def test_chunks(self):
        print(f"Document name: {self.doc_name}")

        response = self.clients.elastic_search().search(index=f"{self.doc_name}-chunk")
        print("Search respond: ", response)
        self.assertIsNotNone(response, "Indexed chunks not found")

        response = self.clients.elastic_search().delete(index=f"{self.doc_name}-chunk")
        print("Deleted chunks: ", response)


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
