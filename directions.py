import csv
import webbrowser
import requests

api_key = 'AIzaSyBFf5FuUH1E8g9dw-R4prdmahjD2wLlKQw'

locations = []
with open('foodie_plan.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        address = row[3] #3 because its the position of address column in the csv file
        encoded_address = requests.utils.quote(address)
        locations.append(encoded_address)
print(locations)

# URL for the Google Maps webpage
google_maps_url = "https://www.google.com/maps/dir/"

# Construct the directions URL by joining the locations
for location in locations:
    google_maps_url += f"{location}/"

# Add your API key to the URL
google_maps_url += f"?key={api_key}"

# Opens the default web browser with the Google Maps URL
webbrowser.open(google_maps_url)
