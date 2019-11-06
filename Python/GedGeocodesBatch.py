import requests
import json as js
import pandas as pd

# Example JSON: https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=315+EAST+5TH+STREET+WATERLOO%2C+IA+50703&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&layer

# Paths
path = '/Users/Fabian/OneDrive/Projekt/GetUSgeocodes/'
file = 'branches_address.csv'

# Data
geodata = pd.DataFrame(pd.read_csv(path + file))

# Prepare Dataset for Upload
geodata['NEWID'] = geodata.index + 1
col_order = ['NEWID', 'street', 'city', 'state', 'zip']
geodata_prepared = geodata.reindex(columns=col_order)

# Partition Dataset into n_j=10,000 large slices and export as .csv
n = geodata_prepared.size

a=b=0
i=1
while b<n:
    b=a+2000
    geodata_partition = geodata_prepared.iloc[a:b]
    geodata_partition.to_csv(path + 'files/part{}.csv'.format(i), index=None, header=False)
    print('part: {} (n={})\t- indexes: {}-{}'.format(i,geodata_partition.size,a,b))
    a = b+1
    i += 1
