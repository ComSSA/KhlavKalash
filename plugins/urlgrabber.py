from plugins.categories import ISilentCommand

import requests
from bs4 import BeautifulSoup

class URLGrabber (ISilentCommand):
    triggers = {r'(http[s]?://\S+)': "url"}

    def run(self, match, context):
        try:
            url = match.group(1)
            response = requests.get(url)
        except (requests.exceptions.ConnectionError) as e:
            print "Failed to load URL: %s" % url
        else:
            soup = BeautifulSoup(response.text)
             
            if soup.title and soup.title.text:
                title = ' '.join(soup.title.string.replace('\n', '').split())
                
                if len(title) > 120:
                    title = title[:117] + "..."
                
                return title
            else:
                print "URL has no title: %s" % url