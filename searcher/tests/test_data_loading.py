from header import *


class TestDataLoading(test.TestCase):
    def setUp(self, root=ROOT):
        vars = ConfigVariables(root)
        db_vars = vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD', 'CA_CERT')
        db_vars['CA_CERT'] = root + db_vars['CA_CERT']
        oai_key = vars.env_vars('OPENAI_API_KEY')
        self.db = ElasticsearchClient(**db_vars)
        self.dims = 5
        self.embedding = OAIEmbeddingClient('text-embedding-3-small', self.dims, **oai_key)

        # self.test_file = "files/Ricardo_Meruane-Noctulo.pdf"
        self.test_file = "../../data/output/documentos-varios.pdf"
        self.doc_name = doc_name_format(self.test_file).title
        self.db.delete(index=self.doc_name)

        # self.chunk_size = 20
        # self.overlap = 1
        self.chunk_size = 20000
        self.overlap = 100
        self.chunks = (Pipeline() | read_pdf(self.test_file)
                                  | chunk(self.chunk_size, self.overlap)
                                  | embed(self.embedding)
                                  | index(self.db)).chunks

    def test_data_ingestion(self):
        num = self.db.client.count(index=self.doc_name)
        print("Number of items: ", num)

        print(f"Document name: {self.doc_name}")
        response = self.db.search(index=self.doc_name, id=0)
        self.assertIsNotNone(response, f"Item with id 0 not found in {self.doc_name} index")
        print("Item: ", response)

        res = self.db.client.search(index=self.doc_name, body={"query": {"match_all": {}}})
        print("All items: ", res)

        response = self.db.search(index=self.doc_name)
        self.assertIsNotNone(response, f"Index {self.doc_name} not found")
        print("Index items: ", response)

        response = self.db.delete(index=self.doc_name)
        print("Delete response: ", response)

    # def test_semantic_search(self):
    #     query = self.embedding.create(input="noctulo")
    #     response = self.db.semantic_search(index=self.doc_name, vector=query, k=1)
    #     self.assertIsNotNone(response, f"Semantic search failed for {query}")
    #     print("Semantic search: ", response)


if __name__ == '__main__':
    test.main(testRunner=RTT())
