from plugins.categories import IRegularCommand

import subprocess
from socket import gethostname

class Uptime (IRegularCommand):
	
	def command_uptime(this, user, channel, *args):
		return "Uptime for %s: " % gethostname() + subprocess.check_output(["uptime"])
