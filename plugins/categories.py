from yapsy.IPlugin import IPlugin

import re

class IRegularCommand (IPlugin):
	name = "Generic Regular Command"
	trigger = []

	def checked_run(self, command, args):
		for trigger in this.triggers:
			if command == trigger:
				return self.run(args)

	def run(self, args):
		pass


class ISilentCommand (IPlugin):
	triggers = {}

	def checked_run(self, msg):
		for trigger in self.triggers:
			match = re.match(trigger, msg)

			if match:
				return self.run(match, self.triggers[trigger])


	def run(self, match, context):
		pass