import rethinkdb as r
from datetime import datetime
from pytz import timezone

con = r.connect()
cursor = r.db('message_archive').table('message_store').filter({'isComplete': 1}).run(con)

# month range of the dataset
month_index = {'Jul': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10, 'Nov': 11}

# Indian Standard Time
ist = timezone('Asia/Calcutta')

# format a hour's int value according to its meridiem
def format_hour(hour, meridiem):
	hour = int(hour)
	if (meridiem == 'pm' and hour != 12):
		hour += 12

	return hour % 24

# calculate delivery time for a order
def calculate_delay(doc):
	order_date = datetime(2015, month_index[doc['orderMonth']], int(doc['orderDay']), format_hour(doc['orderHour'], doc['orderMeridiem']), int(doc['orderMinute']), 0)
	order_date = ist.localize(order_date)

	delivery_date = datetime(2015, month_index[doc['deliveryMonth']], int(doc['deliveryDay']), format_hour(doc['deliveryHour'], doc['deliveryMeridiem']), int(doc['deliveryMinute']), 0)
	delivery_date = ist.localize(delivery_date)

	dt = delivery_date - order_date

	r.db('message_archive').table('message_store').filter({'id': doc['id']}).update({'deliveryDays': dt.days, 'deliverySeconds': dt.total_seconds()}).run(con)

# iterate the process over all the orders
for doc in cursor:
	calculate_delay(doc)
