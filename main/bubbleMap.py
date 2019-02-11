# Libraries
from pymongo import MongoClient
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

# Database Setup
MONGO_HOST= 'mongodb://junekang08:Rf860704!@cluster0-shard-00-00-cnddh.mongodb.net:27017,cluster0-shard-00-01-cnddh.mongodb.net:27017,cluster0-shard-00-02-cnddh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client   = MongoClient(MONGO_HOST)
db       = client.IBDTweets

latitude    = []
longitude   = []
countries   = []
frequency   = []
count = 0

geolocator = Nominatim()

geocodeLim = RateLimiter(geolocator.geocode, min_delay_seconds=1)
georeverseLim = RateLimiter(geolocator.reverse, min_delay_seconds=1)

for document in db.tweet.find({},{"userLocation": 1}):
    userLocation = document.get("userLocation")
    count += 1
    if count % 100 is 0:
        print count
    if userLocation is not None:
        geocode = geocodeLim(userLocation)        
        if geocode is not None:
            coordinates = ", ".join([str(geocode.latitude), str(geocode.longitude)])
            location = georeverseLim(coordinates, language='en')
            if location is not None:
                country = location.raw.get('address').get('country')
                if country not in countries:
                    countries.append(country)
                    latitude.append(geocode.latitude)
                    longitude.append(geocode.longitude)
                    frequency.append(1)
                else:
                    frequency[countries.index(country)] += 1
text_file = open("geo.txt", "w")
text_file.write(str(latitude) + "\n" + str(longitude) + "\n" + str(countries) + "\n" + str(frequency))
text_file.close()

 
# Make a data frame with dots to show on the map
data = pd.DataFrame({
   'lat':latitude,
   'lon':longitude,
   'countries':countries,
   'frequency':frequency
})

# Make an empty map
m = folium.Map(location=[20,0], tiles="Mapbox Bright", zoom_start=2)
 
# I can add marker one by one on the map
for i in range(0,len(data)):
   folium.Circle(
      location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
      popup=data.iloc[i]['countries'],
      radius=data.iloc[i]['frequency']*10000,
      color='crimson',
      fill=True,
      fill_color='crimson'
   ).add_to(m)
 
# Save it as html
m.save('mymap.html')