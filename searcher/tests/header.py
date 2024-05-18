import unittest
import sys
import os
import time
import traceback

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, '../src'))

import utils as log  # noqa: E402
from config import ConfigVariables  # noqa: E402
from clients import Clients  # noqa: E402
from rag import RAG  # noqa: E402
import data_loading  # noqa: E402
from core_classes import Text  # noqa: E402

ROOT = "../"


# NOTA MENTAL (no olvidar): unittest ejecuta el metodo setUp antes de cada test
# por lo tanto, debo eliminar los indices creados en cada test definido
class RichTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = 0

    def startTest(self, test):
        super().startTest(test)
        log.info(f"Starting {test}", "", "")

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes += 1
        log.info(f"Passed {test}", "", "")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        log.error(f"Failed {test}", "", "")
        log.print_traceback(traceback.format_exception(*err))

    def addError(self, test, err):
        super().addError(test, err)
        log.error(f"Error {test}", "", "")
        log.print_traceback(traceback.format_exception(*err))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        log.warning(f"Skipped {test}: {reason}", "", "")

    def stopTestRun(self):
        super().stopTestRun()
        log.info("Test completed", "", "")

    def wasSuccessful(self):
        return self.successes == self.testsRun


class RichTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        sys.stderr = open('/dev/null', 'w')
        super().__init__(*args, stream=sys.stderr, **kwargs)
        self.resultclass = RichTestResult

    def run(self, test):
        time_start = time.time()
        result = super().run(test)
        time_end = time.time()
        total_time = time_end - time_start
        num_successes = result.successes
        num_failures = len(result.failures)
        num_errors = len(result.errors)
        num_skips = len(result.skipped)
        log.pretty_print("Ran C test in C s", result.testsRun, f"{total_time:.2f}")
        print("\n")
        log.pretty_print("Passed: C, Failures: C Errors: C, Skipped: C",
                         num_successes, num_failures, num_errors, num_skips)
        return result
