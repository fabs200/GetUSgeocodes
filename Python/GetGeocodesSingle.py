import pandas as pd
import censusgeocode as cg

# search format: 453 Booth Street, Ottawa ON

# Paths
path = '/Users/Fabian/OneDrive/Projekt/GetUSgeocodes/'
file = 'branches_address.csv'

# Data
geodata = pd.DataFrame(pd.read_csv(path + file))

# Get total size of dataset -1 for indexes
n = geodata.size-1

# Add Searchresult columns
# matchedAddress
geodata['matchedAddress'] = ''
# coordinates
geodata['x'] = ''
geodata['y'] = ''
# tigerline
geodata['tigerLineId'] = ''
geodata['side'] = ''
# 2010 Census Blocks
geodata['SUFFIX'] = ''
geodata['GEOID'] = ''
geodata['CENTLAT'] = ''
geodata['BLOCK'] = ''
geodata['AREAWATER'] = ''
geodata['STATE'] = ''
geodata['BASENAME'] = ''
geodata['OID'] = ''
geodata['LSADC'] = ''
geodata['FUNCSTAT'] = ''
geodata['INTPTLAT'] = ''
geodata['NAME'] = ''
geodata['OBJECTID'] = ''
geodata['TRACT'] = ''
geodata['CENTLON'] = ''
geodata['BLKGRP'] = ''
geodata['AREALAND'] = ''
geodata['INTPTLON'] = ''
geodata['MTFCC'] = ''
geodata['LWBLKTYP'] = ''
geodata['COUNTY'] = ''

# i=1
# searchaddress = geodata['street'].iloc[i] + ' ' + geodata['city'].iloc[i] + ', ' + geodata['state'].iloc[i] + ' ' + str(geodata['zip'].iloc[i])

for i in range(10001, n):

    # Get address
    searchresult = cg.address(street=geodata['street'].iloc[i], city=geodata['city'].iloc[i], state=geodata['state'].iloc[i], zipcode=geodata['zip'].iloc[i])

    percentage = round((i/n), 5)
    print('address {} downloading...\t{}% done'.format(i, percentage))

    # If address search result empty, continue to next, else, save info
    if searchresult is []:
        continue
    else:

        # Save infos
        try:
            geodata.at[i, 'matchedAddress'] = searchresult[0]['matchedAddress']
            geodata.at[i, 'x'] = searchresult[0]['coordinates']['x']
            geodata.at[i, 'y'] = searchresult[0]['coordinates']['y']
            geodata.at[i, 'tigerLineId'] = searchresult[0]['tigerLine']['tigerLineId']
            geodata.at[i, 'side'] = searchresult[0]['tigerLine']['side']
            geodata.at[i, 'SUFFIX'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['SUFFIX']
            geodata.at[i, 'GEOID'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['GEOID']
            geodata.at[i, 'CENTLAT'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['CENTLAT']
            geodata.at[i, 'BLOCK'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['BLOCK']
            geodata.at[i, 'AREAWATER'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['AREAWATER']
            geodata.at[i, 'STATE'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['STATE']
            geodata.at[i, 'BASENAME'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['BASENAME']
            geodata.at[i, 'OID'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['OID']
            geodata.at[i, 'LSADC'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['LSADC']
            geodata.at[i, 'FUNCSTAT'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['FUNCSTAT']
            geodata.at[i, 'INTPTLAT'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['INTPTLAT']
            geodata.at[i, 'NAME'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['NAME']
            geodata.at[i, 'OBJECTID'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['OBJECTID']
            geodata.at[i, 'TRACT'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['TRACT']
            geodata.at[i, 'CENTLON'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['CENTLON']
            geodata.at[i, 'BLKGRP'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['BLKGRP']
            geodata.at[i, 'AREALAND'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['AREALAND']
            geodata.at[i, 'INTPTLON'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['INTPTLON']
            geodata.at[i, 'MTFCC'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['MTFCC']
            geodata.at[i, 'LWBLKTYP'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['LWBLKTYP']
            geodata.at[i, 'COUNTY'] = searchresult[0]['geographies']['2010 Census Blocks'][0]['COUNTY']
        except:
            pass

        if (divmod(i, 10000)[1] == 0) & (i != 0):

            # retrieve part
            part = divmod(i, 2500)[0]

            # Info
            print('address {} reached, now exporting as branches_address_new_p{}.csv, .xlsx'.format(i, part))

            # Export data
            geodata.to_csv(path + 'downloads/branches_address_new_p{}.csv'.format(part), index=None, header=True)
            geodata.to_excel(path + 'downloads/branches_address_new_p{}.xlsx'.format(part), sheet_name='Geo Data', header=True)
