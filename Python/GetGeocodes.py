import requests
import json as js
import pandas as pd

# Example JSON: https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=315+EAST+5TH+STREET+WATERLOO%2C+IA+50703&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&layer

# Paths
path = '/Users/Fabian/OneDrive/Projekt/GetUSgeocodes/'
file = 'branches_address.csv'

# Data
geodata = pd.DataFrame(pd.read_csv(path + file))

# Specify class to get data from API US geocodes
class getgeocodes:
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
        # url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=' + address + '&benchmark=Public_AR_Census2010&vintage=410&format=json'
        url = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=' + address + '&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&layer s=14&format=json'
        return url

    def get_json(self):
        address = self.address
        url = getgeocodes(address).make_url()
        data = requests.get(url).text
        json = js.loads(data)
        return json

    def get_input(self):
        address = self.address
        return getgeocodes(address).get_json()['result']['input']

    def get_matched_address(self):
        address = self.address
        return getgeocodes(address).get_json()['result']['addressMatches'][0]['matchedAddress']

    def get_coordinates(self):
        address = self.address
        return getgeocodes(address).get_json()['result']['addressMatches'][0]['coordinates']

    def get_tigerLine(self):
        address = self.address
        return getgeocodes(address).get_json()['result']['addressMatches'][0]['tigerLine']

    def get_addressComponents(self):
        address = self.address
        return getgeocodes(address).get_json()['result']['addressMatches'][0]['addressComponents']

    def get_CensusBlock(self, keyword=None):
        address = self.address
        self.keyword = keyword
        if keyword is None:
            return getgeocodes(address).get_json()['result']['addressMatches'][0]['geographies']
        if keyword=='States':
            return getgeocodes(address).get_json()['result']['addressMatches'][0]['geographies']['States'][0]
        if keyword=='Counties':
            return getgeocodes(address).get_json()['result']['addressMatches'][0]['geographies']['Counties'][0]
        if keyword=='Census Tracts':
            return getgeocodes(address).get_json()['result']['addressMatches'][0]['geographies']['Census Tracts'][0]
        if keyword=='Census Blocks':
            return getgeocodes(address).get_json()['result']['addressMatches'][0]['geographies']['Census Blocks'][0]

# Add new cols
geodata['matchedAddress'] = ''
geodata['x_coord'] = ''
geodata['y_coord'] = ''
geodata['fromAddress_addressComponents'] = ''
geodata['toAddress_addressComponents'] = ''
geodata['preQualifier_addressComponents'] = ''
geodata['preDirection_addressComponents'] = ''
geodata['preType_addressComponents'] = ''
geodata['streetName_addressComponents'] = ''
geodata['suffixType_addressComponents'] = ''
geodata['suffixDirection_addressComponents'] = ''
geodata['suffixQualifier_addressComponents'] = ''
geodata['city_addressComponents'] = ''
geodata['state_addressComponents'] = ''
geodata['zip_addressComponents'] = ''
geodata['STATENS'] = ''
geodata['COUNTY=Counties'] = ''
geodata['POP100'] = ''
geodata['GEOID'] = ''
geodata['CENTLAT'] = ''
geodata['AREAWATER'] = ''
geodata['STATE'] = ''
geodata['BASENAME'] = ''
geodata['OID'] = ''
geodata['LSADC'] = ''
geodata['FUNCSTAT'] = ''
geodata['INTPLAT'] = ''
geodata['NAME'] = ''
geodata['OBJECTID'] = ''
geodata['TRACT'] = ''
geodata['CENTLON'] = ''
geodata['HU100'] = ''
geodata['AREALAND'] = ''
geodata['INTPTLON'] = ''
geodata['MTFCC'] = ''
geodata['UR'] = ''
geodata['COUNTY'] = ''

# Loop over addresses and get new data
for i in range(0, geodata.size):

    # print
    progress = 100*(i/geodata.size)
    print(progress)

    # Set up address to search for
    searchaddress = geodata['street'].iloc[i] + ' ' + geodata['city'].iloc[i] + ', ' + geodata['state'].iloc[i] + ' ' + str(geodata['zip'].iloc[i])
    # Download json
    geocode = getgeocodes(address=searchaddress)
    # Save Infos
    geodata[i, 'matchedAddress'] = geocode.get_matched_address()
    geodata[i, 'x_coord'] = geocode.get_coordinates()['x']
    geodata[i, 'y_coord'] = geocode.get_coordinates()['y']
    geodata[i, 'fromAddress_addressComponents'] = geocode.get_addressComponents()['fromAddress']
    geodata[i, 'toAddress_addressComponents'] = geocode.get_addressComponents()['toAddress']
    geodata[i, 'preQualifier_addressComponents'] = geocode.get_addressComponents()['preQualifier']
    geodata[i, 'preDirection_addressComponents'] = geocode.get_addressComponents()['preDirection']
    geodata[i, 'preType_addressComponents'] = geocode.get_addressComponents()['preType']
    geodata[i, 'streetName_addressComponents'] = geocode.get_addressComponents()['streetName']
    geodata[i, 'suffixType_addressComponents'] = geocode.get_addressComponents()['suffixType']
    geodata[i, 'suffixDirection_addressComponents'] = geocode.get_addressComponents()['suffixDirection']
    geodata[i, 'suffixQualifier_addressComponents'] = geocode.get_addressComponents()['suffixQualifier']
    geodata[i, 'city_addressComponents'] = geocode.get_addressComponents()['city']
    geodata[i, 'state_addressComponents'] = geocode.get_addressComponents()['state']
    geodata[i, 'zip_addressComponents'] = geocode.get_addressComponents()['zip']
    geodata[i, 'STATENS'] = geocode.get_CensusBlock(keyword='States')['STATENS']
    geodata[i, 'COUNTY'] = geocode.get_CensusBlock(keyword='Counties')['COUNTY']
    geodata[i, 'POP100'] = geocode.get_CensusBlock(keyword='Census Tracts')['POP100']
    geodata[i, 'GEOID'] = geocode.get_CensusBlock(keyword='Census Tracts')['GEOID']
    geodata[i, 'CENTLAT'] = geocode.get_CensusBlock(keyword='Census Tracts')['CENTLAT']
    geodata[i, 'AREAWATER'] = geocode.get_CensusBlock(keyword='Census Tracts')['AREAWATER']
    geodata[i, 'STATE'] = geocode.get_CensusBlock(keyword='Census Tracts')['STATE']
    geodata[i, 'BASENAME'] = geocode.get_CensusBlock(keyword='Census Tracts')['BASENAME']
    geodata[i, 'OID'] = geocode.get_CensusBlock(keyword='Census Tracts')['OID']
    geodata[i, 'LSADC'] = geocode.get_CensusBlock(keyword='Census Tracts')['LSADC']
    geodata[i, 'FUNCSTAT'] = geocode.get_CensusBlock(keyword='Census Tracts')['FUNCSTAT']
    geodata[i, 'INTPLAT'] = geocode.get_CensusBlock(keyword='Census Tracts')['INTPLAT']
    geodata[i, 'NAME'] = geocode.get_CensusBlock(keyword='Census Tracts')['NAME']
    geodata[i, 'OBJECTID'] = geocode.get_CensusBlock(keyword='Census Tracts')['OBJECTID']
    geodata[i, 'TRACT'] = geocode.get_CensusBlock(keyword='Census Tracts')['TRACT']
    geodata[i, 'CENTLON'] = geocode.get_CensusBlock(keyword='Census Tracts')['CENTLON']
    geodata[i, 'HU100'] = geocode.get_CensusBlock(keyword='Census Tracts')['HU100']
    geodata[i, 'AREALAND'] = geocode.get_CensusBlock(keyword='Census Tracts')['AREALAND']
    geodata[i, 'INTPTLON'] = geocode.get_CensusBlock(keyword='Census Tracts')['INTPTLON']
    geodata[i, 'MTFCC'] = geocode.get_CensusBlock(keyword='Census Tracts')['MTFCC']
    geodata[i, 'UR'] = geocode.get_CensusBlock(keyword='Census Tracts')['UR']

# Export data
geodata.to_csv(path + 'branches_address_new.csv', index=None, header=True)
geodata.to_excel(path + 'branches_address_new.xlsx', sheet_name='Geo Data', header=True)

