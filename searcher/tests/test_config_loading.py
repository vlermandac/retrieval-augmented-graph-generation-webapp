from header import *


class TestConfig(unittest.TestCase):
    def setUp(self, root=ROOT):
        self.config_variables = ConfigVariables(root)
        self.expected_config_variables = [
            'unprocessed_files',
            'processed_files',
            'chunk_size',
            'chunk_overlap',
            'chat_model',
            'embedding_model',
            'embedding_dimension',
            'index_name',
            'top_k',
        ]

    def test_config_variables(self):
        temp = self.expected_config_variables

        obtained_variables = self.config_variables(*temp)
        print(obtained_variables)
        self.assertListEqual(list(obtained_variables.keys()),
                             self.expected_config_variables,
                             "The config variables are not as expected")

    def test_update_config(self):
        old_config = self.config_variables(*self.expected_config_variables)
        old_preprocess = PreprocessConfig(
            chunk_size=old_config['chunk_size'],
            chunk_overlap=old_config['chunk_overlap']
        )
        old_llm = LLMConfig(
            chat_model=old_config['chat_model'],
            embedding_model=old_config['embedding_model'],
            embedding_dimension=old_config['embedding_dimension']
        )
        old_rag = RAGConfig(
            index_name=old_config['index_name'],
            top_k=old_config['top_k']
        )
        new_config = Config(
            preprocess=PreprocessConfig(chunk_size=1, chunk_overlap=2),
            llm=LLMConfig(chat_model="3", embedding_model="4", embedding_dimension=5),
            rag=RAGConfig(index_name="6", top_k=7)
        )
        self.config_variables.update_config(new_config)
        obtained_variables = self.config_variables(*self.expected_config_variables)
        print(obtained_variables)
        # self.assertDictEqual(obtained_variables, new_config.dict(),
        #                      "The config variables are not as expected")
        new_config = Config(
            preprocess=old_preprocess,
            llm=old_llm,
            rag=old_rag
        )
        self.config_variables.update_config(new_config)
        print(self.config_variables(*self.expected_config_variables))


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
