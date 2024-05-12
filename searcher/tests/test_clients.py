from header import *


class TestClients(unittest.TestCase):
    def setUp(self, root=ROOT):
        vars = ConfigVariables(root)
        env_var = vars.env_vars('ELASTIC_URL', 'ELASTIC_PASSWORD',
                                'CA_CERT', 'OPENAI_API_KEY')
        cert_mod = root + env_var['CA_CERT']
        env_var['CA_CERT'] = cert_mod
        self.test_clients = Clients(**env_var)

    def test_openai_client(self):
        client = self.test_clients.open_ai()
        self.assertIsNotNone(client)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Your are the happiest assistant in the world!"},
                {"role": "user",
                 "content": "Hello!"}
            ]
        )
        print(response.choices[0].message)
        self.assertIsNotNone(response.choices[0].message)

    def test_elastic_search_client(self):
        client = self.test_clients.elastic_search()

        client.index(index='test-index', id='1', document={'test': 'test'})
        response = client.get(index='test-index', id='1')
        print(response)
        self.assertIsNotNone(response)
        client.indices.delete(index='test-index')


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
