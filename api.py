from utils.utils import DotDict
from endpoint import Endpoint
from restClient import RestClient
from resource import Resource


class API(Resource):
    RESOURCE = "/apis"

    def __init__(self, name, version, context, service_url=None, **kwargs):
        super().__init__()
        self.client = None  # REST API Client
        self.id = None
        self._data = None

        self.name = name
        self.context = context
        self.version = version
        self.endpoint = DotDict()
        if service_url:
            inline_endpoint_name = "{}_{}".format(Endpoint.CONST.TYPES.SANDBOX, name)
            self.endpoint[Endpoint.CONST.TYPES.SANDBOX] = Endpoint(inline_endpoint_name, 'http', service_url)
            inline_endpoint_name = "{}_{}".format(Endpoint.CONST.TYPES.PRODUCTION, name)
            self.endpoint[Endpoint.CONST.TYPES.PRODUCTION] = Endpoint(inline_endpoint_name, 'http', service_url)
        if kwargs:
            self._parse_json(kwargs)

    def set_rest_client(self, client=RestClient()):
        self.client = client

    def save(self):
        if self.id:
            print("WARN: API is already persist")
            return self
        res = self.client.session.post(API.get_endpoint(), json=self.to_json(),
                                       verify=self.client.verify)
        if res.status_code != 201:
            print(res.json())
            raise Exception("An error occurred while creating an API CODE: " + res.status_code)
        self._parse_json(res.json())
        print("Status code: {}".format(res.status_code))
        return self

    def to_json(self):
        temp = {
            'name': self.name,
            'version': self.version,
            'context': self.context,
        }
        endpoints = []
        for type, endpoint in self.endpoint.items():
            serialize_endpoint = {"type": type}
            if endpoint.id:
                serialize_endpoint['key'] = endpoint.id
            else:
                serialize_endpoint['inline'] = endpoint.to_json()
            endpoints.append(serialize_endpoint)
        if len(endpoints):
            temp['endpoint'] = endpoints
        return temp

    def _parse_endpoint(self, endpoint_json):
        for endpoint in endpoint_json:
            endpoint_json = endpoint.get('inline') or endpoint.get('key')
            self.endpoint[endpoint['type']] = Endpoint(**endpoint_json)

    def set_endpoint(self, endpoint_type, endpoint):
        if endpoint_type not in Endpoint.CONST.TYPES.values():
            raise Exception("Endpoint type should be one of these {}".format(Endpoint.CONST.TYPES.values()))
        if type(endpoint) is not Endpoint:
            raise Exception("endpoint should be an instance of Endpoint")
        if endpoint_type != Endpoint.CONST.TYPES.INLINE and not endpoint.id:
            raise Exception("Global endpoint should have persist before mapping it to an API")
        self.endpoint[endpoint_type] = endpoint
        self._data.endpoint = self.endpoint
        res = self.client.session.put(API.get_endpoint() + "/" + self.id, json=self._data, verify=self.client.verify)
        if res.status_code != 200:
            print("Something went wrong when updating endpoints")
            print(res)
        return self

    def set_policies(self, policy_data):
        self.policies = self.policies if self.policies else []
        if type(policy_data) is list:
            self.policies.extend(policy_data)
        else:
            self.policies.append(policy_data)
        self._data["policies"] = self.policies
        res = self.client.session.put(API.get_endpoint() + "/" + self.id, json=self._data, verify=self.client.verify)
        if res.status_code != 200:
            print("Something went wrong when updating policies")
            print(res)
        return self

    def delete(self):
        res = self.client.session.delete(API.get_endpoint() + "/{}".format(self.id), verify=self.client.verify)
        if res.status_code != 200:
            print("Warning Error while deleting the API {}\nERROR: {}".format(self.name, res.content))
        print("Status code: {}".format(res.status_code))

    def change_lc(self, state):
        api_id = self.id
        data = {
            "action": state,
            "apiId": api_id
        }
        lcs = self.client.session.get(API.get_endpoint() + "/{apiId}/lifecycle".format(apiId=api_id))
        if lcs.ok:
            lcs = lcs.json()
            available_transitions = [current_state for current_state in lcs['availableTransitionBeanList'] if
                                     current_state['targetState'] == state]
            if len(available_transitions) == 1:
                res = self.client.session.post(API.get_endpoint() + "/change-lifecycle", params=data,
                                               verify=self.client.verify)
                print("Status code: {}".format(res.status_code))
            else:
                raise ("Invalid transition state valid ones are = {}".format(lcs['availableTransitionBeanList']))
        else:
            raise ("Can't find Lifecycle for the api {}".format(api_id))

    @property
    def _parsers(self):
        parsers = {  # if need special parsing other than simply assigning as attribute
            'endpoint': self._parse_endpoint
        }
        return parsers

    @staticmethod
    def delete_all(client=RestClient()):
        res = client.session.get(API.get_endpoint(), verify=client.verify)
        if not res.status_code == 200:
            print(res.json())
            raise Exception("Error getting APIs list")
        print("Status code: {}".format(res.status_code))
        apis_list = res.json()['list']
        for api in apis_list:
            res = client.session.delete(API.get_endpoint() + "/{}".format(api['id']), verify=client.verify)
            if res.status_code != 200:
                print("Warning Error while deleting the API {}\nERROR: {}".format(api['name'], res.content))
            print("Status code: {}".format(res.status_code))

    @staticmethod
    def all(client=RestClient()):
        res = client.session.get(API.get_endpoint(), verify=client.verify)
        if not res.status_code == 200:
            print(res.json())
            raise Exception("Error getting APIs list")
        print("Status code: {}".format(res.status_code))
        return [API(**api) for api in res.json()['list']]
