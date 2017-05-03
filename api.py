import requests


class RestClient(object):
    def __init__(self):
        self.base_path = "https://localhost:9292"
        self.api_version = 1.0
        self.publisher_api = self.base_path + "/api/am/publisher/v{api_version}".format(api_version=self.api_version)
        self.client_session = requests.Session()
        self.verify = False
        self._getAccessToken()

    def _getAccessToken(self):
        form_data = {
            'username': 'admin',
            'password': 'admin',
            'grant_type': 'password',
            'validity_period': '3600',
            'scopes': 'apim:api_view apim:api_create apim:api_publish apim:tier_view apim:tier_manage apim:subscription_view apim:subscription_block apim:subscribe'
        }
        login = self.client_session.post(self.base_path + "/publisher/auth/apis/login/token", data=form_data,
                                         verify=self.verify)
        if not login.ok:
            print("Error: {}".format(login.reason))
            return False
        self.access_token = self.client_session.cookies['WSO2_AM_TOKEN_1'] + self.client_session.cookies[
            'WSO2_AM_TOKEN_2']
        self.client_session.headers['Authorization'] = 'Bearer ' + self.client_session.cookies['WSO2_AM_TOKEN_1']
        del self.client_session.cookies['WSO2_AM_TOKEN_1']
        del self.client_session.cookies['WSO2_AM_TOKEN_2']
        print("session headers: {}".format(self.client_session.headers))


class Endpoint(RestClient):
    def __init__(self):
        super().__init__()
        self.service_path = self.publisher_api + "/endpoints"

    def addEndpoint(self, data):
        res = self.client_session.post(self.service_path, json=data, verify=self.verify)
        print("Status code: {}".format(res.status_code))
        return res.json()


class API(RestClient):
    def createAPI(self, data):
        endpoint_data = {
            "name": "{}_{}".format(data['name'], data['version']),
            "endpointConfig": "http://www.sample.com/apis/",
            "endpointSecurity": "{'enabled':'true','type':'basic','properties':{'username':'admin','password':'admin'}}",
            "maxTps": 1000,
            "type": "http"
        }
        endpoint = Endpoint().addEndpoint(endpoint_data)
        endpoints = [
            {"id": endpoint['id'], "type": "production"},
            {"id": endpoint['id'], "type": "sandbox"}
        ]
        data['endpoint'] = endpoints
        res = self.client_session.post(self.publisher_api + "/apis", json=data, verify=self.verify)
        print("Status code: {}".format(res.status_code))
        return res.json()

    def deleteAPI(self, uuid):
        res = self.client_session.delete(self.publisher_api + "/apis/{}".format(uuid),
                                         verify=self.verify)
        print("Status code: {}".format(res.status_code))

    def getAll(self):
        res = self.client_session.get(self.publisher_api + "/apis", verify=self.verify)
        print("Status code: {}".format(res.status_code))
        return res.json()

    def deleteAll(self):
        allApis = self.getAll()
        for api in allApis['list']:
            print("Deleting {}".format(api['name']))
            self.deleteAPI(api['id'])

    def changeLC(self, apiId, state):
        data = {
            "action": state,
            "apiId": apiId
        }
        lcs = self.client_session.get(self.publisher_api + "/apis/{apiId}/lifecycle".format(apiId=apiId))
        if lcs.ok:
            lcs = lcs.json()
            available_transitions = [current_state for current_state in lcs['availableTransitionBeanList'] if
                                     current_state['targetState'] == state]
            if len(available_transitions) == 1:
                res = self.client_session.post(self.publisher_api + "/apis/change-lifecycle", params=data,
                                               verify=self.verify)
                print("Status code: {}".format(res.status_code))
            else:
                raise ("Invalid transition state valid ones are = {}".format(lcs['availableTransitionBeanList']))
        else:
            raise ("Can't find Lifecycle for the api {}".format(apiId))
