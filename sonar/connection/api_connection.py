import requests
from requests.auth import HTTPBasicAuth


class APIConnection:

    def __init__(self, server, auth, insecure=True):
        self.session = requests.Session()
        self.server = server
        self.auth = auth
        self.verify = insecure
        self.login()

    def login(self):
        url = self.server + '/api/authentication/login'
        params = {
            'login': self.auth[0],
            'password': self.auth[1]
        }
        self.do_post(
            url=url,
            params=params
        )

    def do_get(self, url, params=None):

        response = self.session.get(
            url=url,
            params=params,
            verify=(self.verify)
        )

        return response

    def do_post(self, url, params=None):
        self.session.post(
            url=url,
            params=params
        )

    def logout(self):
        url = self.server + '/api/authentication/logout'
        self.do_post(url=url)
