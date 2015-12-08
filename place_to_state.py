import requests as r
import re
import json

mail_url = 'https://maps.googleapis.com/maps/api/geocode/json'
payload = {'key': 'AIzaSyALZxIeLuy3sTgiRO8ztoZqHho9Jc3zQwc', 'components': 'country:IN', 'address': ''}

# count of orders in a state
state_count = {}

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
		state_count[_state] += 1
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
					state_count[_state] += 1
				except Exception, e:
					state_count[_state] = 0
				finally:
					place_visited[address_string] = _state
					break

# save the collection
with open('state_count.json', 'w') as f:
	json.dump(state_count, f)