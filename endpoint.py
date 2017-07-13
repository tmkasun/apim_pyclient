import json

from restClient import RestClient
from utils.utils import DotDict

endpoint_const = {
    'SECURITY_TYPES': {'BASIC': "basic", 'DIGEST': 'digest'},
    'TYPES': {
        'PRODUCTION': "production",
        'SANDBOX': "sandbox",
        'INLINE': "inline",
    }
}


class Endpoint(object):
    CONST = DotDict(endpoint_const)

    def __init__(self, name, service_url, endpoint_type, max_tps=10):
        if endpoint_type not in ['http', 'https']:
            raise Exception("endpoint_type should be either http or https")
        self.id = None  # None until persist via REST API, call save() will set ID
        self._data = None  # raw endpoint data

        self.client = None
        self.endpoint_config = {'service_url': service_url}
        self.endpoint_security = {'enabled': False}
        self.name = name
        self.max_tps = max_tps
        self.type = endpoint_type

    def is_secured(self):
        return self.endpoint_security['enabled']

    def set_rest_client(self, client=RestClient()):
        self.client = client

    def set_security(self, security_type, username, password):
        if security_type not in Endpoint.CONST.SECURITY_TYPES.values():
            raise Exception("Invalid security type, please proved one of follows {}".format(Endpoint.CONST.SECURITY_TYPES))
        self.endpoint_security = {
            'enabled': True,
            'type': security_type,
            'username': username,
            'password': password
        }
        return self.endpoint_security

    @property
    def service_url(self):
        yield self.endpoint_config['service_url']

    @service_url.setter
    def service_url(self, value):
        self.endpoint_config['service_url'] = value

    def save(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = self.to_json()
        res = self.client.session.post(self.client.publisher_api + "/endpoints", data=json.dumps(data),
                                       verify=self.client.verify,
                                       headers=headers)
        print("Status code: {}".format(res.status_code))
        if res.status_code != 201:
            print(res.json())
            raise Exception("Fail to save the global endpoint via REST API")
        self._data = DotDict(res.json())
        self.id = self._data.id
        return self

    def delete(self):
        res = self.client.session.delete(self.client.publisher_api + "/endpoints/{}".format(self.id),
                                         verify=self.client.verify)
        if res.status_code != 200:
            print("Warning Error while deleting the API {}\nERROR: {}".format(self.name, res.content))
        print("Status code: {}".format(res.status_code))

    def to_json(self):
        temp = {
            'name': self.name,
            'endpointConfig': json.dumps(self.endpoint_config),
            'endpointSecurity': self.endpoint_security,
            'maxTps': self.max_tps,
            'type': self.type
        }
        return temp

    @staticmethod
    def delete_all(client=RestClient()):
        res = client.session.get(client.publisher_api + "/endpoints", verify=client.verify)
        if not res.status_code == 200:
            print(res.json())
            raise Exception("Error getting APIs list")
        print("Status code: {}".format(res.status_code))
        apis_list = res.json()['list']
        for api in apis_list:
            res = client.session.delete(client.publisher_api + "/endpoints/{}".format(api['id']), verify=client.verify)
            if res.status_code != 200:
                print("Warning Error while deleting the API {}\nERROR: {}".format(api['name'], res.content))
            print("Status code: {}".format(res.status_code))

    @staticmethod
    def all():
        raise NotImplemented("Not implemented yet ...")


def main():
    print("Endpoint testing")
    endpoint = Endpoint("sample_4", "http://www.google.com/sample", "http")
    endpoint.save()


if __name__ == '__main__':
    main()
