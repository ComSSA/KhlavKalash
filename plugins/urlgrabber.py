from plugins.categories import ISilentCommand

try:
    import requests_pyopenssl
    from requests.packages.urllib3 import connectionpool
    connectionpool.ssl_wrap_socket = requests_pyopenssl.ssl_wrap_socket
except ImportError:
    pass

import requests
from bs4 import BeautifulSoup

class URLGrabber (ISilentCommand):
    triggers = {r'.*(http[s]?://[A-Za-z0-9&?%._~!/=+-]+).*': "url"}

    def trigger_url(self, context, user, channel, match):
        try:
            url = match.group(1)
            response = requests.get(url)
        except (requests.exceptions.ConnectionError) as e:
            print "Failed to load URL: %s" % url
	    print "Message: %s" % e
        else:
            soup = BeautifulSoup(response.text)
             
            if soup.title and soup.title.text:
                title = soup.title.string
                title = title.replace('\n', '')    # remove newlines
                title = title.replace('\x01', '')  # remove dangerous control character \001
                title = ' '.join(title.split())    # normalise all other whitespace

                # Truncate length
                if len(title) > 120:
                    title = title[:117] + "..."
                
                return title
            else:
                print "URL has no title: %s" % url
