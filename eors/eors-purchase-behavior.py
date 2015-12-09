import json
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime, timedelta

"""
r.db('message_archive').table('message_store')
	.filter(r.row('orderMonth').eq('Jul').and(r.row('orderDay').eq('17')).or(r.row('orderDay').eq('18')).or(r.row('orderDay').eq('19')).or(r.row('orderDay').eq('20')).or(r.row('orderDay').eq('21')))
	.group('orderHour', 'orderDay', 'orderMeridiem')
	.count()
"""

# format a hour's int value according to its meridiem
def format_hour(hour, meridiem):
	hour = int(hour)
	if (meridiem == 'pm' and hour != 12):
		hour += 12

	return hour % 24

# days containing the 'EORS' period
start_x = datetime(2015, 7, 17)
end_x = datetime(2015, 7, 20)

time_list = [start_x + timedelta(hours=h) for h in range(24 * ((end_x - start_x).days + 1))]

z = [0 for i in range(len(time_list))]

with open('eors_period_order_time.json', 'r') as f:
	order_data = json.loads(f.read())

for order in order_data:
	order_time = order['group']
	order_date = datetime(2015, 7, int(order_time[1]), format_hour(order_time[0], order_time[2]))

	td = order_date - start_x
	index = (td.days * 24) + (td.seconds / 3600)

	z[index] = order['reduction']


data = [
    go.Heatmap(
        z=[z],
        x=time_list,
        y=['Order Density'],
        colorscale='Viridis'
    )
]
plot_url = py.plot(data, filename='eors-purchase-behavior')