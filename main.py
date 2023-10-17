import requests
import csv
import unicodedata

api_key = 'AIzaSyBFf5FuUH1E8g9dw-R4prdmahjD2wLlKQw'

latitude = '33.4255' 
longitude = '-111.9400' 
radius = '5000' #5km radius

# base URL for the Google Places API
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

place_type = 'food'
regular_timings = "10AM - 11PM"
food_trucks = []

# parameters for the API request
params = {
    'location': f'{latitude},{longitude}',
    'radius': radius,
    'type': place_type,
    'keyword': 'food truck',
    'key': api_key,
}

response = requests.get(base_url, params=params)
data = response.json()

# Set up the base URL for the Place Details API
details_base_url = 'https://maps.googleapis.com/maps/api/place/details/json'
#This is done as some timings and websotes for the food trucks are not fetched properly

detailed_food_trucks = []

if 'results' in data:
    for result in data['results']:
        place_id = result['place_id']
        details_params = {
            'placeid': place_id,
            'key': api_key,
        }
        details_response = requests.get(details_base_url, params=details_params)
        details_data = details_response.json()

        if 'result' in details_data:
            detailed_info = details_data['result']
            name = detailed_info['name']
            address = detailed_info.get('vicinity', 'N/A')
            rating = detailed_info.get('rating', 'N/A')
            website = detailed_info.get('website', 'N/A')
            opening_hours = detailed_info.get('opening_hours', {}).get('weekday_text', regular_timings)
            raw_opening_hours = detailed_info.get('opening_hours', {}).get('weekday_text', regular_timings)
            #print(raw_opening_hours,type(raw_opening_hours))
            if "10AM - 11PM" in raw_opening_hours:
                opening_hours = ' '.join([unicodedata.normalize("NFKD", hours) for hours in raw_opening_hours])
            else:
                opening_hours = [unicodedata.normalize("NFKD", hours) for hours in raw_opening_hours]

            cuisine_type = ', '.join(detailed_info.get('types', []))

            detailed_food_trucks.append({
                'name': name,
                'address': address,
                'rating': rating,
                'website': website,
                'opening_hours': opening_hours,
                'cuisine_type': cuisine_type,
            })

with open('food_truck_information_detailed.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'address', 'rating', 'website', 'opening_hours', 'cuisine_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(detailed_food_trucks)
