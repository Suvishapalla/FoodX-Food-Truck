import pandas as pd
import folium
import googlemaps
from datetime import datetime, timedelta

gmaps = googlemaps.Client(key='AIzaSyBFf5FuUH1E8g9dw-R4prdmahjD2wLlKQw')  

food_truck_data = pd.read_csv('food_truck_information_detailed.csv')

foodie_plan = []

# Initialize a Folium map centered at a specific location
m = folium.Map(location=[33.4509195552, -112.113147298], zoom_start=12)

def calculate_travel_info(origin_coords, destination_coords, mode="driving"):
    now = datetime.now()
    directions_result = gmaps.directions(
        (origin_coords['lat'], origin_coords['lng']),
        (destination_coords['lat'], destination_coords['lng']),
        mode=mode,
        departure_time=now
    )
    if not directions_result:
        return None, None, None
    route = directions_result[0]['legs'][0]
    travel_time = route['duration']['text']
    travel_distance = route['distance']['text']
    transport_mode = "Driving" if mode == "driving" else "Walking"
    return travel_time, travel_distance, transport_mode

start_time = datetime.strptime('9:00 AM', '%I:%M %p')
current_day = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
buffer_minutes = 30

visited_food_trucks = set()  

for i in range(len(food_truck_data)):
    for j in range(i + 1, len(food_truck_data)):
        origin = food_truck_data.loc[i, 'address']
        destination = food_truck_data.loc[j, 'address']
        
        origin_geocode = gmaps.geocode(origin)
        destination_geocode = gmaps.geocode(destination)
        
        if origin_geocode and destination_geocode:
            origin_coords = origin_geocode[0]['geometry']['location']
            destination_coords = destination_geocode[0]['geometry']['location']
            
            if food_truck_data.loc[j, 'name'] in visited_food_trucks:
                continue
            
            driving_time, driving_distance, _ = calculate_travel_info(origin_coords, destination_coords, "driving")
            walking_time, walking_distance, _ = calculate_travel_info(origin_coords, destination_coords, "walking")
            
            if driving_time and driving_distance:
                start_time_str = start_time.strftime('%I:%M %p')
                
                # If the next food truck cannot be visited on the same day, move to the next day
                if start_time > current_day.replace(hour=18, minute=0, second=0, microsecond=0):
                    current_day += timedelta(days=1)
                    current_day = current_day.replace(hour=9, minute=0, second=0, microsecond=0)
                    start_time = current_day
                
                foodie_plan.append({
                    'Start Time': start_time_str,
                    'Name': food_truck_data.loc[j, 'name'],
                    'Cuisine': food_truck_data.loc[j, 'cuisine_type'],
                    'Address': destination,
                    'Travel Mode': "Driving",
                    'Travel Distance': driving_distance,
                    'Travel Time': driving_time,
                })
                visited_food_trucks.add(food_truck_data.loc[j, 'name'])
                
                # Create a route on the map just for reference
                folium.PolyLine(
                    locations=[(origin_coords['lat'], origin_coords['lng']),
                               (destination_coords['lat'], destination_coords['lng'])],
                    color='blue',
                    weight=5
                ).add_to(m)
                
                # Calculate the next start time
                travel_minutes = int(driving_time.split(' ')[0])
                start_time += timedelta(minutes=travel_minutes + buffer_minutes)

foodie_plan_df = pd.DataFrame(foodie_plan)

foodie_plan_df.to_csv('foodie_plan.csv', index=False)

m.save('foodie_plan_map.html')

