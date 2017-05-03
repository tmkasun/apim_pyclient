import random, string
from api import API


class APITest(object):
    def __init__(self, debug=True):
        self.debub = debug
        self.api = API()

    def populateAPIs(self, count=10):
        template = {
            "name": None,
            "context": None,
            "version": "1.0.0",
            "apiDefinition": "{ \"paths\": { \"/*\": { \"get\": { \"description\": \"Global Get\" } } }, \"swagger\": \"2.0\" }",
            "cacheTimeout": 10,
            "transport": ["https"],
            "policies": ["Unlimited"],
            "visibility": "PUBLIC",
            "businessInformation": {},
            "corsConfiguration": {}
        }
        apis = []
        for index in range(count):
            random_char = random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
            name_context = "{}sample_{}"
            template['name'] = template['context'] = name_context.format(random_char, index)
            api = self.api.createAPI(template)
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
                self.api.changeLC(api['id'], state)
        else:
            api = apis
            self.api.changeLC(api['id'], state)


def main():
    tester = APITest()
    tester.api.deleteAll()
    apis = tester.populateAPIs(5)
    tester.publishAPIs(apis)


if __name__ == '__main__':
    main()
