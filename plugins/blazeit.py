from plugins.categories import IRegularCommand

import pytz
from datetime import datetime, timedelta
import random

zones = pytz.all_timezones[:]

class BlazeIt (IRegularCommand):
	
	def command_blazeit(this, context, user, channel, args):
		return this.blazeit(4, 20, both=True)
	
	def command_thirteen(this, context, user, channel, args):
		return this.blazeit(13, 13, 13, both=False)
	
	def blazeit(this, h, m, s=0, both=False):
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
				h, m, s
			))
			afternoon = (h >= 11)
			while now > then:
				whole_day = timedelta(1)
				if both or afternoon:
					then = tz.localize(datetime(
						then.year,
						then.month,
						then.day,
						h, m, s
					)) + whole_day
					afternoon = (h >= 11)
				else:
					then = tz.localize(datetime(
						then.year,
						then.month,
						then.day,
						h + 12, m, s
					))
					afternoon = False
			if then - realnow <= min:
				bestid = tzid
				bestthen = then
				min = then - realnow
		wait = (bestthen - realnow).total_seconds()
		(minutes, seconds) = divmod(wait, 60)
		if s > 0:
			timestr = '%d:%02d:%02d' % (h, m, s)
		else:
			timestr = '%d:%02d' % (h, m)
		return 'The next %s is %d:%02d away, in %s (UTC%s)' % (
			timestr, minutes, seconds,
			bestid, bestthen.strftime('%z')
		)
