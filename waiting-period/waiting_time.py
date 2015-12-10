from __future__ import division
from random import randint
import plotly.plotly as py
import plotly.graph_objs as go
import rethinkdb as r
from datetime import datetime, timedelta

con = r.connect()

# for EORS sale
cursor = r.db('message_archive').table('message_store').filter(
	lambda msg:
	((msg['orderMonth'] == 'Jul') & ((msg['orderDay'] == '18') | (msg['orderDay'] == '19')) & ((msg['isComplete'] == 1) | (msg['isReturn'] == 1)))
).run(con)

"""
# total records
cursor = r.db('message_archive').table('message_store').filter(
	lambda msg:
	(((msg['isComplete'] == 1) | (msg['isReturn'] == 1)))
).run(con)
"""

pm = [[] for i in range(24)]
sm = [[] for i in range(24)]

# format a hour's int value according to its meridiem
def format_hour(hour, meridiem):
	hour = int(hour)
	if (meridiem == 'pm' and hour != 12):
		hour += 12
	if (meridiem == 'am' and hour == 12):
		hour = 0

	return hour % 24

for doc in cursor:
	index = format_hour(doc['orderHour'], doc['orderMeridiem'])

	order_time = datetime(2015, 7, int(doc['orderDay']), index, int(doc['orderMinute']))
	events = doc['events']

	# some orders for third party suppliers are packed after sending the information to them
	next_index = 1 if events[1]['remark'] == 'Order is packed' else 2
	pack_event = events[next_index]

	pack_event_time = datetime(2015, 7, int(pack_event['day']), format_hour(pack_event['time'][1:3], pack_event['time'][6:8]), int(pack_event['time'][4:6]), 0)
	packing_delay = pack_event_time - order_time

	next_index += 1
	ship_event = events[next_index]

	ship_event_time = datetime(2015, 7, int(ship_event['day']), format_hour(ship_event['time'][1:3], ship_event['time'][6:8]), int(ship_event['time'][4:6]), 0)
	shipping_delay = ship_event_time - pack_event_time

	if (shipping_delay.days >= 0):
		pm[index].append((packing_delay.days * 24) + (packing_delay.seconds / 3600))
		sm[index].append((shipping_delay.days * 24) + (shipping_delay.seconds / 3600))

for i in range(24):
	pm[i] = sum(pm[i]) / len(pm[i]) if sum(pm[i]) != 0 else 0
	sm[i] = sum(sm[i]) / len(sm[i]) if sum(sm[i]) != 0 else 0

print 'DAILY AVERAGE', sum(pm) / len(pm)
# 8.23737012715 - non sale
# 33.8982553466 - for sale

_x = ['0' + str(i) + ':00' if len(str(i)) < 1 else str(i) + ':00' for i in range(24)]

trace1 = go.Bar(
    x=_x,
    y=pm,
    name='Packing Delay'
)
trace2 = go.Bar(
    x=_x,
    y=sm,
    name='Shipping Delay'
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='stack',
    title='Average Waiting Time in Warehouse',
    xaxis=dict(
        title="Time of the day"
    ),
    yaxis=dict(
        title="Hours"
    ),
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='warehouse-waiting')
