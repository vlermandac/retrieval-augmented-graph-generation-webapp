from header import (
    ConfigVariables, ElasticsearchClient, OAIEmbeddingClient, OAIChatClient,
    Pipeline, ROOT, RTT, read_pdf, chunk, embed, index, doc_name_format, test
)
from triplet import TripletBuilder


class TestTriplets(test.TestCase):

    def setUp(self, root=ROOT):
        # CONFIG VARIABLES
        # Loaded from config and env files
        vars = ConfigVariables(root)
        db_vars = vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD', 'CA_CERT')
        db_vars['CA_CERT'] = root + db_vars['CA_CERT']
        oai_key = vars.env_vars('OPENAI_API_KEY')
        # Manually set
        test_file = "files/Ricardo_Meruane-Noctulo.pdf"
        emb_model = 'text-embedding-3-small'
        chat_model = 'gpt-3.5-turbo'
        dims = 5
        size = 20
        overlap = 1

        # CLIENTS
        self.db = ElasticsearchClient(**db_vars)
        self.llm = OAIChatClient(chat_model, **oai_key)
        embedding = OAIEmbeddingClient(emb_model, dims, **oai_key)

        # DATA LOADING
        self.doc_name = doc_name_format(test_file).title
        self.db.delete(index=self.doc_name)
        (Pipeline() | read_pdf(test_file)
                    | chunk(size, overlap)
                    | embed(embedding)
                    | index(self.db))

    def test_document(self):
        print(self.doc_name)
        chunks = self.db.search(index=self.doc_name)
        print(chunks)
        self.assertIsNotNone(chunks)
        triplets = TripletBuilder(chunks=chunks, llm=self.llm).get_triplets()
        self.assertTrue(triplets)
        print(triplets.model_dump_json(indent=2))


if __name__ == '__main__':
    test.main(testRunner=RTT())
