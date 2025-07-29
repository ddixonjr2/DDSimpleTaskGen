from argparse import ArgumentParser
from messaging_common import DEFAULT_INSTRUCTIONS

class TaskListGen_ArgParser():
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument('--request')
        parser.add_argument('--instructions', default=DEFAULT_INSTRUCTIONS)
        args = parser.parse_args()
        self.request = args.request
        self.instructions = args.instructions
