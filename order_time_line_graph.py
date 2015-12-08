import json
import plotly.plotly as py
import plotly.graph_objs as go

# format a hour's int value according to its meridiem
def format_hour(hour, meridiem):
	hour = int(hour)
	if (meridiem == 'pm' and hour != 12):
		hour += 12

	return hour % 24

# grouped [on (hour, minute, meridiem) triplet] JSON collection
with open('order_time.json', 'r') as f:
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

data = [
    go.Scatter(
        x = x1 + x2,
        y = y1 + y2
    )
]

layout = go.Layout(
    title='When does India shops?',
    yaxis=dict(
        title='No. of Orders',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='order_time_line_graph')