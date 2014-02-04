from plugins.categories import IRegularCommand

import subprocess
from socket import gethostname


class Uptime (IRegularCommand):
	name = "Uptime"
	triggers = ["uptime"]

	def run(this, args):
		return "Uptime for %s: " % gethostname() + subprocess.check_output(["uptime"])
