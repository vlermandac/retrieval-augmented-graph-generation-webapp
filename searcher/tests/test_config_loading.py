from header import *


class TestConfig(unittest.TestCase):
    def setUp(self, root=ROOT):
        self.config_variables = ConfigVariables(root)
        self.expected_config_variables = [
            'data',
            'unprocessed_files',
            'processed_files',
            'preprocess',
            'chunk_size',
            'overlap',
            'embedding',
            'dims',
            'embedding_model',
            'llm',
            'k',
            'test_control_variable',
            'do_not_delete'
        ]

    def test_config_variables(self):
        control_variable = self.config_variables.list['test_control_variable']
        self.assertEqual(control_variable['do_not_delete'], None)

        temp = self.expected_config_variables

        obtained_variables = self.config_variables(*temp)
        print(obtained_variables)
        self.assertListEqual(list(obtained_variables.keys()),
                             self.expected_config_variables,
                             "The config variables are not as expected")


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
