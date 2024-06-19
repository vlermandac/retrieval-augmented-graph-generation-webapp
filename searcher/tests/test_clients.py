from header import *


class TestClients(test.TestCase):
    def setUp(self, root=ROOT):
        vars = ConfigVariables(root)
        db_vars = vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD', 'CA_CERT')
        db_vars['CA_CERT'] = root + db_vars['CA_CERT']
        oai_key = vars.env_vars('OPENAI_API_KEY')
        self.llm = OAIChatClient('gpt-3.5-turbo', **oai_key)
        self.embedding = OAIEmbeddingClient('text-embedding-3-small', 200, **oai_key)
        self.db = ElasticsearchClient(**db_vars)

    def chat_model(self, llm: LLM) -> str:
        response = llm.inference(
            messages=[
                {"role": "system",
                 "content": "Your are the happiest assistant in the world!"},
                {"role": "user",
                 "content": "Hello!"}
            ]
        )
        return response

    def test_chat_model(self):
        self.assertIsNotNone(self.llm.client)
        response = self.chat_model(self.llm)
        print(response)
        self.assertIsNotNone(response)

    def embedding_model(self, embedding: EmbeddingModel, text: str) -> List[float]:
        return embedding.create(input=text)

    def test_embedding_model(self):
        self.assertIsNotNone(self.embedding.client)
        response = self.embedding_model(self.embedding, 'test text')
        print(response)
        self.assertIsNotNone(response)

    def database(self, db: Database, index: str, item: TextItem):
        db.index(index=index, item=item)
        response = db.search(index=index, id=item.id)
        self.assertIsNotNone(response, f"Item with id {item.id} not found in {index} index")

        db.delete(index=index, id=item.id)
        response = db.search(index=index, id=item.id)
        self.assertIsNone(response, f"Item was not correctly deleted from {index} index")

        response = db.search(index=index)
        print(f"Index {index} after item deletion: {response}")
        self.assertTrue(len(response) == 0, f"Index {index} is not empty after item deletion")

        db.delete(index=index)
        response = db.search(index=index)
        self.assertIsNone(response, f"Index {index} was not correctly deleted")

    def test_elastic_search_client(self):
        self.assertIsNotNone(self.db.client)
        self.database(
            self.db, 'test-index', TextItem(id='test-id', text='test text')
        )


if __name__ == '__main__':
    test.main(testRunner=RTT())
