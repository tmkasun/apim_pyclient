import json

from restClient import RestClient
from utils.utils import DotDict
from resource import Resource

endpoint_const = {
    'SECURITY_TYPES': {'BASIC': "basic", 'DIGEST': 'digest'},
    'TYPES': {
        'PRODUCTION': "production",
        'SANDBOX': "sandbox",
        'INLINE': "inline",
    }
}


class Endpoint(Resource):
    CONST = DotDict(endpoint_const)
    RESOURCE = "/endpoints"

    def __init__(self, name, type, service_url='', maxTps=10, **kwargs):
        super().__init__()
        if type not in ['http', 'https']:
            raise Exception("endpoint_type should be either http or https")

        self.endpointConfig = {
            "endpointType": "SINGLE",
            "list": [
                {
                    "url": service_url,
                    "timeout": "1000",
                    "attributes": []
                }
            ]
        }
        self.endpointSecurity = {'enabled': False}
        self.name = name
        self.max_tps = maxTps
        self.type = type
        if kwargs:
            self._parse_json(kwargs)

    def is_secured(self):
        return self.endpointSecurity['enabled']

    def set_rest_client(self, client=RestClient()):
        self.client = client

    def set_security(self, security_type, username, password):
        if security_type not in Endpoint.CONST.SECURITY_TYPES.values():
            raise Exception(
                "Invalid security type, please proved one of follows {}".format(Endpoint.CONST.SECURITY_TYPES))
        self.endpointSecurity = {
            'enabled': True,
            'type': security_type,
            'username': username,
            'password': password
        }
        return self.endpointSecurity

    @property
    def _parsers(self):
        parsers = {
            # 'endpointConfig': self._parse_endpointConfig
        }
        return parsers

    def _parse_endpointConfig(self, value):
        endpoint_config_json = json.loads(value)
        self.endpointConfig = DotDict(endpoint_config_json)

    @property
    def service_url(self):
        return self.endpointConfig['list'][0]['url']

    @service_url.setter
    def service_url(self, value):
        self.endpointConfig['list'][0]['url'] = value

    def save(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = self.to_json()
        res = self.client.session.post(Endpoint.get_endpoint(), data=json.dumps(data), verify=self.client.verify,
                                       headers=headers)
        print("Status code: {}".format(res.status_code))
        if res.status_code != 201:
            print(res.json())
            raise Exception("Fail to save the global endpoint via REST API")
        self._data = DotDict(res.json())
        self.id = self._data.id
        return self

    def delete(self):
        res = self.client.session.delete(Endpoint.get_endpoint(
        ) + "/{}".format(self.id), verify=self.client.verify)
        if res.status_code != 200:
            print("Warning Error while deleting the API {}\nERROR: {}".format(
                self.name, res.content))
        print("Status code: {}".format(res.status_code))

    def to_json(self):
        temp = {
            'name': self.name,
            'endpointConfig': self.endpointConfig,
            'endpointSecurity': self.endpointSecurity,
            'maxTps': self.max_tps,
            'type': self.type
        }
        return temp

    @staticmethod
    def delete_all(client=RestClient()):
        res = client.session.get(Endpoint.get_endpoint(), verify=client.verify)
        if not res.status_code == 200:
            print(res.json())
            raise Exception("Error getting APIs list")
        print("Status code: {}".format(res.status_code))
        apis_list = res.json()['list']
        for api in apis_list:
            res = client.session.delete(Endpoint.get_endpoint(
            ) + "/{}".format(api['id']), verify=client.verify)
            if res.status_code != 200:
                print("Warning Error while deleting the API {}\nERROR: {}".format(
                    api['name'], res.content))
            print("Status code: {}".format(res.status_code))

    @staticmethod
    def all():
        raise NotImplemented("Not implemented yet ...")


def main():
    print("Endpoint testing")
    endpoint = Endpoint("sample_4", "http", "http://www.google.com/sample")
    endpoint.save()


if __name__ == '__main__':
    main()
