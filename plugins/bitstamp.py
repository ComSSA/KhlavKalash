from plugins.categories import IRegularCommand

import bitstamp.client

class Bitstamp (IRegularCommand):
	def __init__(this):
		this.client = bitstamp.client.Public()

	def command_btc(this, context, user, channel, args):
		t = this.client.ticker()
		if len(args) == 0:
	   		returnval = "Bitstamp: \x02Last:\x0F %s \x02Bid:\x0F %s \x02High:\x0F %s \x02Low:\x0F %s \x02Ask:\x0F %s." \
			% (t['last'], t['bid'], t['high'], t['low'], t['ask'])
		elif len(args)  == 1:
			price = str(float(t['ask']) * float(args[0]))
			returnval = "%s bitcoins is worth approx %s" \
			% (args[0], price)
		
		return returnval
