import requests
import json as js
import pandas as pd

path = '/Users/Fabian/OneDrive/Projekt/USgeocodes/'
file = 'branches_address.csv'

geodata = pd.DataFrame(pd.read_csv(path + file))

class getgeocodes:
    """
    returns json after specifying address in the format '4600 Silver Hill Rd, Suitland, MD 20746”'
    """
    def __init__(self, address):
        self.address = address

    def make_url(self, address):
        self.address = address
        # Convert spaces to plus signs
        address = address.replace(' ', '+')
        # Convert comma to %2C
        address = address.replace(',', '%2C')
        # url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address='+address+'&benchmark=9&format=json'
        url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address='+address+'&benchmark=Public_AR_Census2010&format=json'
        return url

    def get_json(self, address):
        self.address = address
        url = self.make_url(address)
        data = requests.get(url).text
        json = js.loads(data)
        return json_example['result']

    def json_input(self, json):
        json_result = self.get_json(json)
        json_input = json_result['result']['input']



address_example = geodata['street'].iloc[0] + ' ' + geodata['city'].iloc[0] + ', ' + geodata['state'].iloc[0] + ' ' + str(geodata['zip'].iloc[0])
url_example = getgeocodes(address=address_example).make_url(address=address_example)
json_example = getgeocodes(address=address_example).get_json(address=address_example)
json_example['result']


class Dog:

    tricks = []             # mistaken use of a class variable

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)


