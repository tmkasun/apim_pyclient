import requests


class RestClient(object):
    _instance = None

    def __init__(self):
        self.base_path = "https://localhost:9292"
        self.session = requests.Session()
        self.verify = False
        self._get_access_token()
        RestClient._client = self

    def _get_access_token(self):
        form_data = {
            'username': 'admin',
            'password': 'admin',
            'grant_type': 'password',
            'validity_period': '3600',
            'scopes': 'apim:api_view apim:api_create apim:api_publish apim:tier_view apim:tier_manage apim:subscription_view apim:subscription_block apim:subscribe'
        }
        login = self.session.post(self.base_path + "/login/token/publisher", data=form_data,
                                  verify=self.verify)
        if not login.ok:
            print("Error: {}".format(login.reason))
            return False
        self.access_token = self.session.cookies['WSO2_AM_TOKEN_1'] + self.session.cookies[
            'WSO2_AM_TOKEN_2']
        self.session.headers['Authorization'] = 'Bearer ' + self.session.cookies['WSO2_AM_TOKEN_1']
        del self.session.cookies['WSO2_AM_TOKEN_1']
        del self.session.cookies['WSO2_AM_TOKEN_2']
        print("session headers: {}".format(self.session.headers))
