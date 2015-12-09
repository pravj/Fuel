import requests as r
import re
import json

mail_url = 'https://maps.googleapis.com/maps/api/geocode/json'
#payload = {'key': 'AIzaSyALZxIeLuy3sTgiRO8ztoZqHho9Jc3zQwc', 'components': 'country:IN', 'address': ''}
payload = {'key': 'AIzaSyDxgwEwLseBS58clOpKVVF466iyc5YkHG4', 'components': 'country:IN', 'address': ''}

# JSON data source (collected from rethinkdb), place and respective order counts
with open('place_order_count.json', 'r') as f:
	places = json.loads(f.read())

# alphabetic regex pattern
pattern = re.compile('\w+')

# final co-ordinates for customer locations
address_points = []
# locations resulting in false positive (gives lat/lng for India, zero mile stone)
false_points = []

# available co-ordinates [to prevent duplicate entries]
visited_cords = set()

# iterate over all (distinct) places
for place in places:
	main_location = place['group'].lower()

	# remove alphabetic noise
	location = re.sub('_dc|-|_|,', ' ', main_location)
	# remove delivery centers abbreviations (of length 3)
	location = re.sub('\s+\w{3}$|\d+|cod|centre|service', '', location)

	# address string to be used in the place lookup
	address_string = '+'.join(pattern.findall(location))

	payload['address'] = address_string

	res = r.get(mail_url, params=payload)
	res = res.json()

	if (len(res['results']) > 0):
		address_components = res['results'][0]['address_components']
		if ((len(address_components) == 1) and ('country' in address_components[0]['types'])):
			false_points.append([cords['lat'], cords['lng'], main_location])
			print 'FALSE', main_location, location, cords['lat'], cords['lng']
		else:
			cords = res['results'][0]['geometry']['location']
			cord_tuple = (cords['lat'], cords['lng'])
			if cord_tuple not in visited_cords:
				visited_cords.add(cord_tuple)

				print main_location, location, cords['lat'], cords['lng']
				address_points.append([cords['lat'], cords['lng'], main_location])

with open('customer_locations.json', 'w') as f:
	f.write(json.dumps(address_points))

with open('false_customer_locations.json', 'w') as f:
	f.write(json.dumps(false_points))
