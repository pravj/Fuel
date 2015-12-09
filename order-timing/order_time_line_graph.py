import json
import plotly.plotly as py
from plotly.graph_objs import *

# format a hour's int value according to its meridiem
def format_hour(hour, meridiem):
	hour = int(hour)
	if (meridiem == 'pm' and hour != 12):
		hour += 12

	return hour % 24

# create data lists for a particular type ['complete', 'cancel', 'return']
def prepare_list(filename):
	# grouped [on (hour, minute, meridiem) triplet] JSON collection
	with open(filename, 'r') as f:
		data = json.loads(f.read())

	# X(time) and Y(orders) axis data
	x1, x2 = [], []
	y1, y2 = [], []

	# populate the data lists
	for i in range(1, len(data)):
		timing = data[i]['group']
		meridiem = timing[2]

		if meridiem == 'pm':
			x2.append('%d:%s:00' % (format_hour(timing[0], meridiem), timing[1]))
			y2.append(data[i]['reduction'])
		else:
			x1.append('%d:%s:00' % (format_hour(timing[0], meridiem), timing[1]))
			y1.append(data[i]['reduction'])

	return [x1 + x2, y1 + y2]

# data lists for 'completed' and 'returned' orders
complete_data = prepare_list('complete_order_time.json')
return_data = prepare_list('return_order_time.json')

# completed orders
part1 = Bar(
	x = complete_data[0],
	y = complete_data[1],
	marker=Marker(
        color='#005869'
    ),
    name='Complete Orders',
)

# returned orders
part2 = Bar(
	x = return_data[0],
	y = return_data[1],
	marker=Marker(
        color='#8DB500'
    ),
    name='Returned Orders',
)

data = Data([part1, part2])

layout = Layout(
    title='When does India shops?',
    legend=dict(
        x=1,
        y=1,
        traceorder='normal',
        font=dict(
            family='sans-serif',
            size=12,
            color='#000'
        ),
        bgcolor='#DDDDDD',
        bordercolor='#FFFFFF',
        borderwidth=2
    ),
    yaxis=dict(
        title='No. of Orders',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='order_time_line_graph')