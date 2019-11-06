import requests
import json as js
import pandas as pd

path = '/Users/Fabian/OneDrive/Projekt/GetUSgeocodes/'
file = 'branches_address.csv'

geodata = pd.DataFrame(pd.read_csv(path + file))

class getgeocodes(object):
    """
    returns json after specifying address in the format '4600 Silver Hill Rd, Suitland, MD 20746”'
    """
    def __init__(self, address):
        self.address = address

    def make_url(self):
        address = self.address
        address = address.replace(' ', '+')
        address = address.replace(',', '%2C')
        # url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address='+address+'&benchmark=9&format=json'
        url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address='+address+'&benchmark=Public_AR_Census2010&format=json'
        return url

    def get_json(self):
        address = self.address
        url = getgeocodes(address).make_url()
        data = requests.get(url).text
        json = js.loads(data)
        return json['result']

    def get_matched_address(self):
        address = self.address
        return getgeocodes(address).get_json()['addressMatches'][0]['matchedAddress']

    def get_coordinates(self):
        address = self.address
        return getgeocodes(address).get_json()['addressMatches'][0]['coordinates']

    def get_tigerLine(self):
        address = self.address
        return getgeocodes(address).get_json()['addressMatches'][0]['tigerLine']

    def get_tigerLine(self):
        address = self.address
        return getgeocodes(address).get_json()['addressMatches'][0]['tigerLine']


address_example = geodata['street'].iloc[0] + ' ' + geodata['city'].iloc[0] + ', ' + geodata['state'].iloc[0] + ' ' + str(geodata['zip'].iloc[0])
geocode_example = getgeocodes(address=address_example)
url_example = getgeocodes(address=address_example).make_url()
json_example = getgeocodes(address=address_example).get_json()

jsoninput_example = getgeocodes(address=address_example).get_json()
matchedaddress_example = getgeocodes(address=address_example).get_matched_address()
coordinates_example = getgeocodes(address=address_example).get_coordinates()

geocode_example.get_coordinates()
geocode_example.get_matched_address()
geocode_example.get_tigerLine()
