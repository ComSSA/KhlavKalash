from yapsy.IPlugin import IPlugin
import re

class IRegularCommand (IPlugin):
	def run(self, command, args):
		try:
			return getattr(self, "command_" + command)(args)
		except AttributeError as e:
			pass


class ISilentCommand (IPlugin):
	triggers = {}

	def run(self, user, channel, msg):
		output = []

		for trigger in self.triggers:
			match = re.match(trigger, msg)

			if match:
				try:
					current_output = getattr(self, "trigger_" + self.triggers[trigger])(user, channel, match)
					if current_output is not None:
						output.append(current_output)
				except AttributeError as e:
					pass

		return output
