import requests
from pprint import pprint

class ApiRatp:
    def __init__(self):
        self.headers = {
            'accept': 'application/json',
        }
        self.url = 'https://api-ratp.pierre-grimaud.fr/v4'

    def call(self, arg):
        return requests.get(
                f"{self.url}/{arg}",
                headers=self.headers).json()
    def getBuses(self):
        return self.call("lines/buses")["result"]["buses"]

api = ApiRatp()

pprint(
    list(map(lambda b: b["name"], api.getBuses()))
)