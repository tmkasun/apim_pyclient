import requests
from configs import default
from requests.auth import HTTPBasicAuth


class RestClient(object):
    _instance = None
    APP_SCOPES = {
        "publisher": 'apim:api_view apim:api_create apim:api_publish apim:tier_view apim:tier_manage apim:subscription_view apim:subscription_block apim:subscribe',
        "store": 'apim:subscribe apim:signup apim:workflow_approve'
    }

    def __init__(self, application_name="publisher"):
        self.application_name = application_name
        self.base_path = "https://{host}:{port}".format(
            host=default['connection']['hostname'], port=default['connection']['port'])
        self.session = requests.Session()
        self.verify = False
        self.create_application()
        self._get_access_token()
        RestClient._client = self

    def _get_access_token(self):
        form_data = {
            'username': 'admin',
            'password': 'admin',
            'grant_type': 'password',
            'scope': self.get_scopes_for_app()
        }
        token_endpoint = self.base_path + "/oauth2/token"
        token_response = requests.post(
            token_endpoint, data=form_data, verify=self.verify, auth=(self.application['clientId'], self.application['clientSecret']))
        if not token_response.ok:
            print("Error: {}".format(token_response.reason))
            return False
        # This is to ignore the environment prefix and get the token value
        self.tokens = token_response.json()
        access_token = self.tokens['access_token']
        print("DEBUG: Access token = {}".format(access_token))
        self.session.headers['Authorization']='Bearer ' + access_token
        print("session headers: {}".format(self.session.headers))

    def create_application(self):
        try:
            return self.application
        except:
            print("Haven't done DCR so far so continue . . .")
        dcr_payload={
            "callbackUrl": "www.knnect.com",
            "clientName": "rest_api_publisher",
            "owner": "admin",
            "grantType": "password refresh_token",
            "saasApp": True
        }
        dcr_endpoint=self.base_path + "/client-registration/v0.14/register".format(
            host=default['connection']['hostname'], port=default['connection']['port'])
        dcr_response=requests.post(
            dcr_endpoint, json=dcr_payload, verify=self.verify, auth=("admin", "admin"))
        print(dcr_response)
        if dcr_response.ok:
            self.application=dcr_response.json()
            return self.application
        else:
            raise Exception("Something went wrong while doing DCR endpoint = {} \n payload = {} ".format(
                dcr_endpoint, dcr_payload))

    def get_scopes_for_app(self):
        return RestClient.APP_SCOPES[self.application_name]


# stuff to run always here such as class/def
def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
