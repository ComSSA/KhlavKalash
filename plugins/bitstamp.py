from plugins.categories import IRegularCommand

import bitstamp.client

class Bitstamp (IRegularCommand):
	def __init__(this):
		this.client = bitstamp.client.Public()

	def command_btc(this, user, channel, args):
		t = this.client.ticker()

		# This looks absolutely disgusting
		return "Bitstamp: \x02Last:\x0F %s \x02Bid:\x0F %s \x02High:\x0F %s \x02Low:\x0F %s \x02Ask:\x0F %s." \
		% (t['last'], t['bid'], t['high'], t['low'], t['ask'])