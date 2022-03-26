from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='Your_Name')
location = geolocator.geocode('Patna')
print(location.latitude, location.longitude)