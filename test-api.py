#! /usr/bin/env python3.5
import random, string
from api import API
from endpoint import Endpoint
from restClient import RestClient
from simple_endpoint import EndpointHandler


class APITest(object):
    def __init__(self, debug=True):
        self.debub = debug
        self.client = RestClient()

    def populateAPIs(self, count=10):
        """
        "apiDefinition": "{ \"paths\": { \"/*\": { \"get\": { \"description\": \"Global Get\" } } }, \"swagger\": \"2.0\" }",
            "cacheTimeout": 10,
            "transport": ["https"],
            "policies": ["Unlimited"],
            "visibility": "PUBLIC",
            "businessInformation": {},
            "corsConfiguration": {}
        :param count: 
        :return: 
        """
        template = {
            "name": None,
            "context": None,
            "version": "1.0.0",
            "service_url": "http://sample.knnect.com/api/endpoint"
        }
        apis = []
        for index in range(count):
            random_char = random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
            name_context = "{}_sample_{}".format(random_char, index)
            template['name'] = name_context
            template['context'] = "/" + name_context
            api = API(**template)
            api.set_rest_client(self.client)
            api.save()
            apis.append(api)
        return apis

    def publishAPIs(self, apis, state="Published"):
        """

        :param apis: List of APIs or single API object returned from API.createAPI method
        :param state: State string of the api need to be hange to
        :return:
        """
        if type(apis) is list:
            for api in apis:
                api.change_lc(state)
        else:
            api = apis
            api.change_lc(state)

    def delete_all(self):
        API.delete_all(self.client)

    def delete_all_endpoints(self):
        Endpoint.delete_all(self.client)

    def populate_global_endpoints(self, count=20):
        endpoint_types = ['basic', 'digest']
        endpoints = []
        for index in range(count):
            random_char = random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
            name = "{}_sample_endpoint_{}".format(random_char, index)
            service_url = "https://sample.knnect.com/api/endpoint/" + name
            max_tps = random.randint(1, 1000)
            endpoint = Endpoint(name, "http", service_url, max_tps)
            rand_endpoint = endpoint_types[random.randint(0, 1)]
            endpoint.set_security(rand_endpoint, name, "sample_password")
            endpoint.set_rest_client(self.client)
            endpoint.save()
            endpoints.append(endpoint)
        return endpoints


def main():
    tester = APITest()

    print("INFO: Deleting existing APIs ...")
    tester.delete_all()

    print("INFO: Deleting existing Endpoints ...")
    tester.delete_all_endpoints()

    print("INFO: Creating new APIs ...")
    apis = tester.populateAPIs(15)
    api = API.get(apis[0].id)
    print("INFO: Creating new Global endpoints ...")
    endpoints = tester.populate_global_endpoints(25)
    endpoint = Endpoint.get(endpoints[0].id)

    print("INFO: Publishing newly created APIs ...")
    tester.publishAPIs(apis)

    EndpointHandler.run()


if __name__ == '__main__':
    main()
