from restClient import RestClient
from utils.utils import DotDict


class Resource(object):
    """
    Parent for API and Endpoint resources , implement generalize delete type method here
    """
    BASE = "https://localhost:9292/api/am/"
    VERSION = 1.0
    APPLICATION = "publisher"
    RESOURCE = ''

    def __init__(self):
        self._data = None  # raw Resource data
        self.id = None  # Resource ID, None until persist via REST API, call save() will set ID
        self.client = None

    def delete(self):
        pass

    def _parse_json(self, json_response):
        self._data = DotDict(json_response)
        if not self._data.id:
            raise Exception("JSON response should have id property for a valid Resource")
        for key, val in self._data.items():
            if key in self._parsers:
                self._parsers[key](val)
                continue
            self.__setattr__(key, val)

    @property
    def _parsers(self):
        raise NotImplemented()

    @classmethod
    def get_endpoint(cls):
        return cls.BASE + "{application}/v{api_version}".format(api_version=cls.VERSION,
                                                                application=cls.APPLICATION) + cls.RESOURCE

    @classmethod
    def get(cls, resource_id, client=RestClient()):
        res = client.session.get(cls.get_endpoint() + "/{}".format(resource_id), verify=client.verify)
        if res.status_code != 200:
            print("Warning Error while getting the Resource {}\nERROR: {}".format(resource_id, res.content))
        print("Status code: {}".format(res.status_code))
        return cls(**res.json())

    @staticmethod
    def all():
        pass

    @staticmethod
    def delete_all(self):
        pass
