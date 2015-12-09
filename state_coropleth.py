import json

with open('maps/india_states.geojson', 'r') as f:
	geojson_data = json.loads(f.read())

with open('state_order_count.json', 'r') as f:
	order_data = json.loads(f.read())

for state in geojson_data['features']:
	props = state['properties']
	state_name = props['NAME_1']

	try:
		state['properties'] = {'name': state_name, 'density': order_data[state_name]}
	except Exception, e:
		state['properties'] = {'name': state_name, 'density': 0}
		
		if state_name == 'Uttarakhand':
			state['properties'] = {'name': state_name, 'density': 75}

with open('maps/india_states_1.geojson', 'w') as f:
	json.dump(geojson_data, f)