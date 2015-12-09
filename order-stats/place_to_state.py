import requests as r
import re
import json

mail_url = 'https://maps.googleapis.com/maps/api/geocode/json'
payload = {'key': 'AIzaSyALZxIeLuy3sTgiRO8ztoZqHho9Jc3zQwc', 'components': 'country:IN', 'address': ''}

# count of places in a state
state_place_count = {}
# count of orders in a state
state_order_count = {}

# in-memory cache to reduce the network calls
place_visited = {}

# JSON data source (collected from rethinkdb), place and respective order counts
with open('place_order_count.json', 'r') as f:
	places = json.loads(f.read())

# alphabetic regex pattern
pattern = re.compile('\w+')

# iterate over all (distinct) places
for place in places:
	location = place['group'].lower()

	# remove alphabetic noise
	location = re.sub('_dc|-|_|,', ' ', location)
	# remove delivery centers abbreviations (of length 3)
	location = re.sub('\s+\w{3}$|cod|centre', '', location)

	# address string to be used in the place lookup
	address_string = '+'.join(pattern.findall(location))

	# place already known
	try:
		_state = place_visited[address_string]
		state_place_count[_state] += 1
		state_order_count[_state] += place['reduction']
	except Exception, e:
		payload['address'] = address_string

		res = r.get(mail_url, params=payload)
		res = res.json()

		# iterate backward iteration to make it less than O(n/2). Except single element, obvi.
		components = res['results'][0]['address_components']
		for comp in components[::-1]:
			if 'administrative_area_level_1' in comp['types']:

				_state = comp['long_name']

				try:
					# same state present, because of a different address in the state
					state_place_count[_state] += 1
					state_order_count[_state] += place['reduction']
				except Exception, e:
					state_place_count[_state] = 0
					state_order_count[_state] = 0
				finally:
					place_visited[address_string] = _state
					break

# save the collection of places
with open('state_place_count.json', 'w') as f:
	json.dump(state_place_count, f)

# save the collection of orders
with open('state_order_count.json', 'w') as f:
	json.dump(state_order_count, f)