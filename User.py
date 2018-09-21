import requests
from configs import default
from requests.auth import HTTPBasicAuth
from utils.utils import DotDict

class User(object):

    def __init__(self, userName, password=None, **kwargs):
        self.auth = HTTPBasicAuth(
            default["admin"]["name"], default["admin"]["password"])
        self.userName = userName
        self.password = password
        self.api_endpoint = "https://{host}:{port}/api/identity/scim2/v1.0/Users".format(
            host=default['connection']['hostname'], port=default['connection']['port'])
        self.verify = False
        if kwargs:
            self._parse_json(kwargs)

    def serialize(self):
        data = {
            "name": {
                "familyName": "{}".format(self.userName),
                "givenName": "sam"
            },
            "userName": "{}".format(self.userName),
            "password": "{}123".format(self.userName),
            "emails": [{
                "primary": True,
                "value": "{}@gmail.com".format(self.userName),
                "type": "home"
            },
                {
                "value": "{}_work@wso2.com".format(self.userName),
                "type": "work"
            }
            ]
        }
        if self.password:
            data["password"] = self.password

        return data

    def _parse_json(self, json_response):
        self._data = DotDict(json_response)
        if not self._data.id:  # TODO: Should be able to pass non-preserved api JSON object as well ?
            print("WARN: Missing User ID for parsing data")
            self._data.id = None
            # raise Exception(
            #     "JSON response should have id property for a valid Resource")
        for key, val in self._data.items():
            self.__setattr__(key, val)

    def save(self):
        response = requests.post(
            self.api_endpoint, json=self.serialize(), auth=self.auth, verify=self.verify)
        if not response.ok:
            print(response.content)
            print(response.status_code)
            raise Exception(
                "An error occurred while creating an user: " + str(response.status_code))
        self._parse_json(response.json())
        return self

    def delete(self):
        response = requests.delete(
            "{}/{}".format(self.api_endpoint, self.id), auth=self.auth, verify=self.verify)
        if not response.ok:
            print(response.content)
            print(response.status_code)
            raise Exception(
                "An error occurred while creating an user: " + str(response.status_code))
        return True

    @staticmethod
    def all():
        api_endpoint = "https://{host}:{port}/api/identity/scim2/v1.0/Users".format(
            host=default['connection']['hostname'], port=default['connection']['port'])
        response = requests.get(
            api_endpoint, auth=HTTPBasicAuth(
                default["admin"]["name"], default["admin"]["password"]), verify=False)
        if not response.ok:
            print(response.content)
            print(response.status_code)
            raise Exception(
                "An error occurred while getting all users: " + str(response.status_code))
        return [User(**user) for user in response.json()['Resources']]

    @staticmethod
    def delete_all():
        for user in User.all():
            if user.userName.lower() == 'admin':
                print("WARN: Skip deleting admin user")
                continue
            print("DEBUG: deleting user {}".format(user.userName))
            user.delete()
