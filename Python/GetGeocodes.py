import requests
import json as js
import pandas as pd

path = '/Users/Fabian/OneDrive/Projekt/GetUSgeocodes/'
file = 'branches_address.csv'

geodata = pd.DataFrame(pd.read_csv(path + file))

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


address_example = geodata['street'].iloc[0] + ' ' + geodata['city'].iloc[0] + ', ' + geodata['state'].iloc[0] + ' ' + str(geodata['zip'].iloc[0])
geocode_example = getgeocodes(address=address_example)
url_example = getgeocodes(address=address_example).make_url()
json_example = getgeocodes(address=address_example).get_json()

input_example = getgeocodes(address=address_example).get_input()
matchedaddress_example = getgeocodes(address=address_example).get_matched_address()
coordinates_example = getgeocodes(address=address_example).get_coordinates()
addressComponents_example = geocode_example.get_addressComponents()
censusblock_example = getgeocodes(address=address_example).get_CensusBlock()

geocode_example.get_matched_address()
geocode_example.get_coordinates()
geocode_example.get_tigerLine()
geocode_example.get_addressComponents()
geocode_example.get_CensusBlock()
geocode_example.get_CensusBlock(keyword='States')
geocode_example.get_CensusBlock(keyword='Counties')
geocode_example.get_CensusBlock(keyword='Census Tracts')
geocode_example.get_CensusBlock(keyword='Census Blocks')


######################## Add Columns to Dataframe ########################

# geocode_example.get_matched_address() -> str()
geodata['matchedAddress'] = ''
# geocode_example.get_coordinates() -> {'x': -92.33376, 'y': 42.498493}
geodata['x_coord'] = ''
geodata['y_coord'] = ''
# geocode_example.get_addressComponents() -> {'fromAddress': '301', 'toAddress': '399', 'preQualifier': '', 'preDirection': 'E', 'preType': '', 'streetName': '5th', 'suffixType': 'St', 'suffixDirection': '', 'suffixQualifier': '', 'city': 'WATERLOO', 'state': 'IA', 'zip': '50703'}
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

# geocode_example.get_CensusBlock(keyword='States') -> {'STATENS': '01779785', 'POP100': 3046355, 'GEOID': '19', 'CENTLAT': '+42.0753607', 'AREAWATER': 1076595005, 'STATE': '19', 'BASENAME': 'Iowa', 'STUSAB': 'IA', 'OID': 2749058169487, 'LSADC': '00', 'FUNCSTAT': 'A', 'INTPTLAT': '+42.0700243', 'DIVISION': '4', 'NAME': 'Iowa', 'REGION': '2', 'OBJECTID': 43, 'CENTLON': '-093.4958444', 'AREALAND': 144669296857, 'INTPTLON': '-093.4933473', 'HU100': 1336417, 'MTFCC': 'G4000', 'UR': ''}
# geocode_example.get_CensusBlock(keyword='Census Blocks') -> {'SUFFIX': '', 'POP100': 3, 'GEOID': '190130001002031', 'CENTLAT': '+42.4990817', 'BLOCK': '2031', 'AREAWATER': 0, 'STATE': '19', 'BASENAME': '2031', 'OID': 210404020269037, 'LSADC': 'BK', 'FUNCSTAT': 'S', 'INTPTLAT': '+42.4990817', 'NAME': 'Block 2031', 'OBJECTID': 3414850, 'TRACT': '000100', 'CENTLON': '-092.3339740', 'BLKGRP': '2', 'AREALAND': 13363, 'HU100': 21, 'INTPTLON': '-092.3339740', 'MTFCC': 'G5040', 'LWBLKTYP': 'L', 'UR': '', 'COUNTY': '013'}
# geodata['STATENS_CensusBlock'] = ''
# geodata['POP100_CensusBlock'] = ''
# geodata['GEOID_CensusBlock'] = ''
# geodata['CENTLAT_CensusBlock'] = ''
# geodata['AREAWATER_CensusBlock'] = ''
# geodata['STATE_CensusBlock'] = ''
# geodata['BASENAME_CensusBlock'] = ''
# geodata['STUSAB_CensusBlock'] = ''
# geodata['OID_CensusBlock'] = ''
# geodata['LSADC_CensusBlock'] = ''
# geodata['FUNCSTAT_CensusBlock'] = ''
# geodata['INTPTLAT_CensusBlock'] = ''
# geodata['DIVISION_CensusBlock'] = ''
# geodata['NAME_CensusBlock'] = ''
# geodata['REGION_CensusBlock'] = ''
# geodata['OBJECT_CensusBlock'] = ''
# geodata['CENTLON_CensusBlock'] = ''
# geodata['AREALAND_CensusBlock'] = ''
# geodata['INTPTLON_CensusBlock'] = ''
# geodata['HU100_CensusBlock'] = ''
# geodata['MTFCC_CensusBlock'] = ''
# geodata['UR_CensusBlock'] = ''

# geocode_example.get_CensusBlock(keyword='Counties') -> {'POP100': 131090, 'GEOID': '19013', 'CENTLAT': '+42.4700217', 'AREAWATER': 17900114, 'STATE': '19', 'BASENAME': 'Black Hawk', 'OID': 27590331280582, 'LSADC': '06', 'FUNCSTAT': 'A', 'INTPTLAT': '+42.4728884', 'NAME': 'Black Hawk County', 'OBJECTID': 2600, 'CENTLON': '-092.3087941', 'COUNTYCC': 'H1', 'COUNTYNS': '00465196', 'AREALAND': 1465333940, 'INTPTLON': '-092.3060590', 'HU100': 55887, 'MTFCC': 'G4020', 'UR': '', 'COUNTY': '013'}
geodata['COUNTY=Counties'] = ''

# geocode_example.get_CensusBlock(keyword='Census Tracts') -> {'POP100': 2011, 'GEOID': '19013000100', 'CENTLAT': '+42.5012412', 'AREAWATER': 195173, 'STATE': '19', 'BASENAME': '1', 'OID': 20790331301561, 'LSADC': 'CT', 'FUNCSTAT': 'S', 'INTPTLAT': '+42.5011890', 'NAME': 'Census Tract 1', 'OBJECTID': 25966, 'TRACT': '000100', 'CENTLON': '-092.3367782', 'HU100': 1090, 'AREALAND': 1906200, 'INTPTLON': '-092.3371673', 'MTFCC': 'G5020', 'UR': '', 'COUNTY': '013'}
geodata['POP100'] = ''
geodata['GEOID'] = ''
geodata['CENTLAT'] = ''
geodata['AREAWATER'] = ''
geodata['STATE'] = ''
geodata['BASENAME'] = ''
geodata['OID'] = ''
geodata['LSAD'] = ''
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

