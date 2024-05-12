import argparse
import sys


class Arguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def __or__(self, arg_name):
        self.parser.add_argument(arg_name)
        return self

    def __call__(self):
        if len(sys.argv) != 2:
            self.parser.print_help()
            sys.exit(1)
        return self.parser.parse_args()
