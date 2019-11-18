import pandas as pd
import censusgeocode as cg
import timer
import time
import sys, os
from time import gmtime, strftime

### Get further geo data of addresses in the format: '453 Booth Street, Ottawa ON' from from USCensus

# File with Addresses
file = 'branches_address.csv'

# Get Path where this Script is located
path = os.path.dirname(sys.argv[0])

# Check whether file 'branches_address.csv' exists
if os.path.isfile(path + '/' + file) is True:
    print('file {} found!'.format(file))
else:
    sys.exit('file {} not found! Make sure this Python Script is in the same directory as {} and retry.'.format(file, file))

print('Enter a starting index number, e.g. 10001')
start = int(input())

# Create a destination folder where the downloaded geo data will be saved to
# set up folder name
downloadfolder = strftime('{}_%d%m%Y_%H%M%S'.format(start), gmtime()) # folder naming convention: i_DDMMYY_HHMMSS
# set up destination folder
destinationpath = path + '/' + downloadfolder + '/'
# make directory
try:
    os.mkdir(destinationpath)
except OSError:
    print('Creation of the directory {} failed'.format(destinationpath))
else:
    print('Successfully created the directory {}'.format(destinationpath))

# Load data
geodata = pd.DataFrame(pd.read_csv(path + '/' + file))

# Get total size of dataset for indexes
#n = geodata.shape[0]
n = geodata.tail(1).index[0] + 1

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

# Measure Starting time
startingtime = time.time()

# Info
print('#######\tstart index: {}\n#######\tstart time: {}\n#######\tdestination folder: {}\n'.format(start, strftime('%H%M', gmtime()), destinationpath))

for i in range(start, n):
    print(i, n)
    # Get address
    searchresult = cg.address(street=geodata['street'].iloc[i], city=geodata['city'].iloc[i], state=geodata['state'].iloc[i], zipcode=geodata['zip'].iloc[i])

    percentage = round((i/n), 5)
    sys.stdout.write("\033[F") # Cursor up one line
    print('address {} downloading...\t{} done'.format(i, percentage))

    # If address search result empty, continue to next, else, save info
    if searchresult is []:

        # Info
        print('\t\n no results found! Retrying downloading ...')

        # wait 3 sec and retry, if then still empty, continue
        timer.sleep(3)
        searchresult = cg.address(street=geodata['street'].iloc[i], city=geodata['city'].iloc[i], state=geodata['state'].iloc[i], zipcode=geodata['zip'].iloc[i])

        if searchresult is []:
            print('\t\n no results found!')
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

        if (divmod(i, 2500)[1] == 0) & (i != 0):

            # retrieve part
            part = divmod(i, 2500)[0]

            # Time
            endingtime = time.time()

            # Info
            print('\naddress {} reached, now exporting as branches_address_new_p{}.xlsx (.csv)'.format(i, part))
            print('\nelapsed time: {} seconds\n'.format(round(endingtime-startingtime)))

            # Export data
            geodata.to_csv(destinationpath + 'branches_address_new_p{}.csv'.format(part), header=True)
            geodata.to_excel(destinationpath + 'branches_address_new_p{}.xlsx'.format(part), sheet_name='Geo Data', header=True)

        if i == geodata.tail(1).index[0]:

            # write final part
            part = 'final_part'

            # Time
            endingtime = time.time()

            # Info
            print('\naddress {} reached, now exporting as branches_address_new_{}.xlsx (.csv)'.format(i, part))
            print('\ntotal elapsed time: {} minutes\n'.format(round((endingtime-startingtime)/3600)))

            # Export data
            geodata.to_csv(destinationpath + 'branches_address_new_{}.csv'.format(part), header=True)
            geodata.to_excel(destinationpath + 'branches_address_new_{}.xlsx'.format(part), sheet_name='Geo Data', header=True)

            # finalize
            print('final part saved as branches_address_new_{}.csv (.xlsx)'.format(part))
            print('all done!')
