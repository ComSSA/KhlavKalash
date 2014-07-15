from plugins.categories import IRegularCommand

import urllib
import json

class Google (IRegularCommand):
	
	def command_google(this, context, user, channel, args):
		# Make request
		search = urllib.urlencode({'q': ' '.join(args)})
		url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % search
		responseText = urllib.urlopen(url).read()

		# Parse json into object
		responseJson = json.loads(responseText)

		# Get top result
		data = responseJson['responseData']
		topResult = data['results'][0]
		
		# Print top result info to channel
		return "%s: %s" % (topResult['titleNoFormatting'], topResult['unescapedUrl'])
