import json

from restClient import RestClient
from utils.utils import DotDict
from resource import Resource

application_const = {
    'SECURITY_TYPES': {'BASIC': "basic", 'DIGEST': 'digest'},
    'TYPES': {
        'PRODUCTION': "production",
        'SANDBOX': "sandbox",
        'INLINE': "inline",
    }
}


class Application(Resource):
    CONST = DotDict(application_const)
    RESOURCE = "/applications"
    APPLICATION = "store"

    def __init__(self, name, description, throttlingTier='', **kwargs):
        super().__init__()
        self.name = name
        self.description = description
        self.throttlingTier = throttlingTier

        self.subscriber = None
        self.permission = "[{\"groupId\" : 1000, \"permission\" : [\"READ\",\"UPDATE\"]},{\"groupId\" : 1001, \"permission\" : [\"READ\",\"UPDATE\"]}]"
        self.lifeCycleStatus = None
        self.keys = []
        if kwargs:
            self._parse_json(kwargs)

    def save(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = self.to_json()
        res = self.client.session.post(Application.get_endpoint(), data=json.dumps(data), verify=self.client.verify,
                                       headers=headers)
        print("Status code: {}".format(res.status_code))
        if res.status_code != 201:
            print(res.json())
            raise Exception("Fail to save the global endpoint via REST API")
        self._data = DotDict(res.json())
        self.id = self._data.applicationId
        return self

    @staticmethod
    def delete_all(client=RestClient()):
        res = client.session.get(Application.get_endpoint(), verify=client.verify)
        if not res.status_code == 200:
            print(res.json())
            raise Exception("Error getting Applications list")
        print("Status code: {}".format(res.status_code))
        apps_list = res.json()['list']
        for app in apps_list:
            res = client.session.delete(Application.get_endpoint() + "/{}".format(app['applicationId']), verify=client.verify)
            if res.status_code != 200:
                print("Warning Error while deleting the API {}\nERROR: {}".format(app['name'], res.content))
            print("Status code: {}".format(res.status_code))

    # TODO: Make this a generic to_json method for all Resources
    def to_json(self):
        temp = {
            'name': self.name,
            'description': self.description,
            'throttlingTier': self.throttlingTier
        }
        return temp

    def set_rest_client(self, client=RestClient(APPLICATION)):
        self.client = client
