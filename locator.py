from geopy.geocoders import Nominatim
import requests, json
from secrets import Secret
from tabulate import tabulate
import pandas as pd

secret = Secret()
api_key = secret.key

geolocator = Nominatim(user_agent="geopy first app")
input_location = input('What is the destination address?\n')
current_location = geolocator.geocode(input_location)
current_location_string = str(current_location.latitude) + ',' + str(current_location.longitude)
#print(location.address)
#print((location.latitude, location.longitude))

def get_nearby( types=['restaurant'],radius = '10000' ):
    nearby = []
    for type in types:
        nearby_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
        nearby_response = requests.get( nearby_url + current_location_string + 
                                        '&radius=' + radius + '&types=' + type + '&key=' + api_key )
        nearby.append( nearby_response.json() )
    return nearby

def get_distance_and_duration( current, destination ):
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
    full_url = url + 'origins=' + current + '&units=imperial' + '&destinations=' + destination + '&key=' + api_key
    result_distance = requests.get( full_url ) 

    return ( result_distance.json()['rows'][0]['elements'][0]['distance']['text'], 
            result_distance.json()['rows'][0]['elements'][0]['duration']['text'] )

to_check = ['restaurant','transit_station','supermarket']
nearby_results = get_nearby(to_check)

print('Important waypoints near ' + input_location + ':' )
for i,result in enumerate(nearby_results):
    table = pd.DataFrame({'Name:':[], 'Distance:':[], 'Drive Time:':[]})
    for location in result['results']:
        name = location['name']
        location_lat = str(location['geometry']['location']['lat'])
        location_lng = str(location['geometry']['location']['lng'])
        destination_string = str(location_lat) + ',' + str(location_lng)

        distance, duration = get_distance_and_duration( current_location_string, destination_string )
        new_row = {'Name:':name, 'Distance:': distance, 'Drive Time:': duration}
        table = table.append(new_row, ignore_index=True)
        
    print(to_check[i])
    print(tabulate(table.sort_values(by='Distance:'), headers='keys', tablefmt='psql', showindex=False))
