from plugins.categories import IRegularCommand

import pytz
from datetime import datetime, timedelta
import random

zones = pytz.all_timezones[:]

class BlazeIt (IRegularCommand):
	
	def command_blazeit(this, context, user, channel, args):
		random.shuffle(zones)
		realnow = datetime.now(pytz.timezone('Etc/UTC'))
		bestid = None
		bestthen = None
		min = timedelta.max
		for tzid in zones:
			tz = pytz.timezone(tzid)
			now = datetime.now(tz)
			then = tz.localize(datetime(
				now.year,
				now.month,
				now.day,
				4, 20
			))
			afternoon = False
			while not then > now:
				delta = timedelta(1)
				if afternoon:
					then = tz.localize(datetime(
						then.year,
						then.month,
						then.day,
						4, 20
					)) + delta
				else:
					then = tz.localize(datetime(
						then.year,
						then.month,
						then.day,
						16, 20
					))
				afternoon = not afternoon
			if then - realnow <= min:
				bestid = tzid
				bestthen = then
				min = then - realnow
		wait = (bestthen - realnow).total_seconds()
		(minutes, seconds) = divmod(wait, 60)
		return ('The next 4:20 is in ' + bestid + ' (UTC' +
			bestthen.strftime('%z') +
			'), ' + str(int(minutes)) + ' minutes and ' +
			str(int(seconds)) + ' seconds from now')
