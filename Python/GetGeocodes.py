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
class GetGeocodeJSON:
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
        url = GetGeocodeJSON(address).make_url()
        data = requests.get(url).text
        # If no json could be retrieved, make an empty json
        try:
            json = js.loads(data)
        except:
            json = {'result': {'addressMatches': []}}
        return json

    def get_input(self):
        address = self.address
        return GetGeocodeJSON(address).get_json()['result']['input']

    def get_matched_address(self):
        address = self.address
        return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['matchedAddress']

    def get_coordinates(self):
        address = self.address
        return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['coordinates']

    def get_tigerLine(self):
        address = self.address
        return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['tigerLine']

    def get_addressComponents(self):
        address = self.address
        return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['addressComponents']

    def get_CensusBlock(self, keyword=None):
        address = self.address
        self.keyword = keyword
        if keyword is None:
            return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['geographies']
        if keyword=='States':
            return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['geographies']['States'][0]
        if keyword=='Counties':
            return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['geographies']['Counties'][0]
        if keyword=='Census Tracts':
            return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['geographies']['Census Tracts'][0]
        if keyword=='Census Blocks':
            return GetGeocodeJSON(address).get_json()['result']['addressMatches'][0]['geographies']['Census Blocks'][0]

def get_Geodata(geodataJSON, keyword=None):
    if keyword is None:
        return geodataJSON

    # First check whether matchedAddress is non-empty
        # first check if empty = no result
        if geodataJSON['result']['addressMatches'] == [] is True:
            return 'NA'
        else:
            # matchedAddress
            if keyword=='matchedAddress':
                return geodataJSON['result']['addressMatches'][0]['matchedAddress']
            if keyword=='x_coord':
                return geodataJSON['result']['addressMatches'][0]['coordinates']['x']
            if keyword=='y_coord':
                return geodataJSON['result']['addressMatches'][0]['coordinates']['y']
            if keyword=='tigerLine':
                return geodataJSON['result']['addressMatches'][0]['tigerLine']

            # addressComponent
            if keyword=='fromAddress':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['fromAddress']
            if keyword=='preQualifier':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['preQualifier']
            if keyword=='preDirection':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['preDirection']
            if keyword=='preType':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['preType']
            if keyword=='streetName':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['streetName']
            if keyword=='suffixType':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['suffixType']
            if keyword=='suffixDirection':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['suffixDirection']
            if keyword=='suffixQualifier':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['suffixQualifier']
            if keyword=='city':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['city']
            if keyword=='state':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['state']
            if keyword=='zip':
                return geodataJSON['result']['addressMatches'][0]['addressComponents']['zip']

            # States
            if keyword=='STATENS':
                return geodataJSON['result']['addressMatches'][0]['geographies']['States'][0]['STATENS']

            # Census Tracts
            if keyword=='POP100':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['POP100']
            if keyword=='GEOID':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['GEOID']
            if keyword=='CENTLAT':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['CENTLAT']
            if keyword=='AREAWATER':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['AREAWATER']
            if keyword=='STATE':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['STATE']
            if keyword=='BASENAME':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['BASENAME']
            if keyword=='OID':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['OID']
            if keyword=='LSADC':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['LSADC']
            if keyword=='FUNCSTAT':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['FUNCSTAT']
            if keyword=='INTPLAT':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['INTPLAT']
            if keyword=='NAME':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['NAME']
            if keyword=='OBJECTID':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['OBJECTID']
            if keyword=='TRACT':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['TRACT']
            if keyword=='CENTLON':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['CENTLON']
            if keyword=='HU100':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['HU100']
            if keyword=='AREALAND':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['AREALAND']
            if keyword=='INTPTLON':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['INTPTLON']
            if keyword=='MTFCC':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['MTFCC']
            if keyword=='UR':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['UR']

            # Census Block
            if keyword=='COUNTY':
                return geodataJSON['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['COUNTY']

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

### Loop over addresses and get new data

# TEMPÖ Make 10 parts
k = 10
t = int(1/k * geodata.size)
p1 = range(0, t)
p2 = range(t, t+2)
p3 = range(t+3, t+4)
p4 = range(t+4, t+5)
p5 = range(t+5, t+6)
p6 = range(t+6, t+7)
p7 = range(t+7, t+8)
p8 = range(t+8, t+9)
p9 = range(t+9, t+10)
p10 = range(t+10, geodata.size)


# modulus counter, once it reaches 250, geodata is saved and moduluscounter is set back to 0
moduluscounter=0

# for i in range(0, geodata.size):
for i in p1:

    # Set up address to search for
    searchaddress = geodata['street'].iloc[i] + ' ' + geodata['city'].iloc[i] + ', ' + geodata['state'].iloc[i] + ' ' + str(geodata['zip'].iloc[i])

    # print
    progress = round(100*(i/geodata.size), 5)
    print('observation {}/{} - {}% - search address: {}'.format(i, geodata.size, progress, searchaddress))

    # Download json
    json = GetGeocodeJSON(address=searchaddress).get_json()

    # Save Infos
    geodata.loc[i, 'matchedAddress'] = get_Geodata(json, keyword='matchedAddress')
    geodata.loc[i, 'x_coord'] = get_Geodata(json, keyword='x_coord')
    geodata.loc[i, 'y_coord'] = get_Geodata(json, keyword='y_coord')
    geodata.loc[i, 'fromAddress_addressComponents'] = get_Geodata(json, keyword='fromAddress')
    geodata.loc[i, 'toAddress_addressComponents'] = get_Geodata(json, keyword='toAddress')
    geodata.loc[i, 'preQualifier_addressComponents'] = get_Geodata(json, keyword='preQualifier')
    geodata.loc[i, 'preDirection_addressComponents'] = get_Geodata(json, keyword='preDirection')
    geodata.loc[i, 'preType_addressComponents'] =get_Geodata(json, keyword='preType')
    geodata.loc[i, 'streetName_addressComponents'] = get_Geodata(json, keyword='streetName')
    geodata.loc[i, 'suffixType_addressComponents'] = get_Geodata(json, keyword='suffixType')
    geodata.loc[i, 'suffixDirection_addressComponents'] = get_Geodata(json, keyword='suffixDirection')
    geodata.loc[i, 'suffixQualifier_addressComponents'] = get_Geodata(json, keyword='suffixQualifier')
    geodata.loc[i, 'city_addressComponents'] = get_Geodata(json, keyword='city')
    geodata.loc[i, 'state_addressComponents'] = get_Geodata(json, keyword='state')
    geodata.loc[i, 'zip_addressComponents'] = get_Geodata(json, keyword='zip')
    geodata.loc[i, 'STATENS'] = get_Geodata(json, keyword='STATENS')
    geodata.loc[i, 'COUNTY'] = get_Geodata(json, keyword='COUNTY')
    geodata.loc[i, 'POP100'] = get_Geodata(json, keyword='POP100')
    geodata.loc[i, 'GEOID'] = get_Geodata(json, keyword='GEOID')
    geodata.loc[i, 'CENTLAT'] = get_Geodata(json, keyword='CENTLAT')
    geodata.loc[i, 'AREAWATER'] = get_Geodata(json, keyword='AREAWATER')
    geodata.loc[i, 'STATE'] = get_Geodata(json, keyword='STATE')
    geodata.loc[i, 'BASENAME'] = get_Geodata(json, keyword='BASENAME')
    geodata.loc[i, 'OID'] = get_Geodata(json, keyword='OID')
    geodata.loc[i, 'LSADC'] = get_Geodata(json, keyword='LASADC')
    geodata.loc[i, 'FUNCSTAT'] = get_Geodata(json, keyword='FUNCSTAT')
    geodata.loc[i, 'INTPLAT'] = get_Geodata(json, keyword='INTPLANT')
    geodata.loc[i, 'NAME'] = get_Geodata(json, keyword='NAME')
    geodata.loc[i, 'OBJECTID'] = get_Geodata(json, keyword='OBJECTID')
    geodata.loc[i, 'TRACT'] = get_Geodata(json, keyword='TRACT')
    geodata.loc[i, 'CENTLON'] = get_Geodata(json, keyword='CENTLON')
    geodata.loc[i, 'HU100'] = get_Geodata(json, keyword='HU100')
    geodata.loc[i, 'AREALAND'] = get_Geodata(json, keyword='AREALAND')
    geodata.loc[i, 'INTPTLON'] = get_Geodata(json, keyword='INTPTLON')
    geodata.loc[i, 'MTFCC'] = get_Geodata(json, keyword='MTFCC')
    geodata.loc[i, 'UR'] = get_Geodata(json, keyword='UR')

    # Export data each i=250 entries
    moduluscounter += 1
    if moduluscounter == 250:

        # Display message for saving
        print('saving file for first {} entries'.format(i))

        # Export data
        geodata.to_csv(path + 'branches_address_new_p1.csv', index=None, header=True)
        geodata.to_excel(path + 'branches_address_new_p1.xlsx', sheet_name='Geo Data', header=True)
        # Set back to 0
        moduluscounter = 0
