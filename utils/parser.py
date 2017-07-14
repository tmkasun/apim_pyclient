import json
from utils.utils import DotDict


class Parser(object):
    def __init__(self, key):
        self.key = key

    def parse(self, value):
        return DotDict(json.loads(value))

    def serializer(self, value):
        return json.dumps(value)
