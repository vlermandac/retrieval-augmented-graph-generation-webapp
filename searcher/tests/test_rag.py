from header import *


class TestRAG(test.TestCase):
    def setUp(self, root=ROOT):

        # CONFIG VARIABLES
        # Loaded from config and env files
        vars = ConfigVariables(root)
        db_vars = vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD', 'CA_CERT')
        db_vars['CA_CERT'] = root + db_vars['CA_CERT']
        oai_key = vars.env_vars('OPENAI_API_KEY')
        # Manually set
        test_file = "files/Ricardo_Meruane-Noctulo.pdf"
        dims = 5
        size = 20
        overlap = 1

        # CLIENTS
        db = ElasticsearchClient(**db_vars)
        embedding = OAIEmbeddingClient('text-embedding-3-small', dims, **oai_key)
        llm = OAIChatClient('gpt-3.5-turbo', **oai_key)

        # DATA LOADING
        self.doc_name = doc_name_format(test_file).title
        db.delete(index=self.doc_name)
        self.chunks = (Pipeline() | read_pdf(test_file)
                                  | chunk(size, overlap)
                                  | embed(embedding)
                                  | index(db)).chunks

        # RAG
        self.rag = RAG(
            db=db,
            llm=llm,
            embedding=embedding,
            index_name=self.doc_name,
            top_k=1
        )

    def test_generation(self):
        rag_response = self.rag(query="What does it seems to be the main topic of the text?")
        print(rag_response)
        self.assertIsNotNone(rag_response)


if __name__ == '__main__':
    test.main(testRunner=RTT())
