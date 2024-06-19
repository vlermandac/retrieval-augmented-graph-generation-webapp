import unittest as test
import sys
import os
import logging
from typing import List, Dict

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, '../src'))

from config import ConfigVariables  # noqa
from clients import (
    ElasticsearchClient, OAIEmbeddingClient, OAIChatClient
)  # noqa
from data_ingestion import (
    Pipeline, read_pdf, chunk, embed, index
)  # noqa
from core_classes import (
    TextItem, Config, EditableOptions, PreprocessConfig, LLMConfig, RAGConfig,
    EmbeddingModel, LLM, Database
)  # noqa
from rag import RAG  # noqa
from utils import doc_name_format  # noqa

ROOT = "../"
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

__all__ = [
    'ConfigVariables', 'ElasticsearchClient', 'OAIEmbeddingClient',
    'OAIChatClient', 'Pipeline', 'read_pdf', 'chunk', 'embed', 'index',
    'TextItem', 'Config', 'EditableOptions', 'RAG',
    'doc_name_format', 'ROOT', 'log', 'test', 'RichTestResult',
    'RTT', 'LLMConfig', 'RAGConfig', 'PreprocessConfig',
    'EmbeddingModel', 'LLM', 'Database', 'List', 'Dict'
]


class RichTestResult(test.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = 0

    def startTest(self, test):
        super().startTest(test)
        log.info(f"Starting {test}\n")

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes += 1
        log.info(f"Passed {test}\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        log.info(f"Failed {test}\n")

    def addError(self, test, err):
        super().addError(test, err)
        log.info(f"Error {test}\n")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        log.info(f"Skipped {test}: {reason}\n")

    def stopTestRun(self):
        super().stopTestRun()
        log.info("Test completed\n")

    def wasSuccessful(self):
        return self.successes == self.testsRun


class RTT(test.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resultclass = RichTestResult

    def run(self, test):
        result = super().run(test)
        num_successes = result.successes
        num_failures = len(result.failures)
        num_errors = len(result.errors)
        num_skips = len(result.skipped)
        log.info(
            f"""
            Passed: {num_successes}, Failures: {num_failures},
            Errors: {num_errors}, Skipped: {num_skips}
            \n"""
        )
        return result


if __name__ == "__main__":
    # Discover and run all tests in the 'tests' directory
    loader = test.TestLoader()
    suite = loader.discover(start_dir='.')

    # Run the test suite
    runner = RTT()
    result = runner.run(suite)
