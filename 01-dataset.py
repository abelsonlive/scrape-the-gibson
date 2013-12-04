import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin
import dataset


# A list of missed connections in New York
BASE_URL = 'http://newyork.craigslist.org/'

database = dataset.connect('sqlite:///missed_connections.db')

table = database['missed_connections']

def scrape_missed_connections():
    """ Scrape all the deputies from the list """
    
    # Download the list.
    response = requests.get(BASE_URL + "mis/")

    # Parse HTML
    soup = BeautifulSoup(response.content)

    # Get all the links to missed connections:
    for missed_connection in soup.find_all('span', {'class':'pl'}):
        
        link = missed_connection.find('a').attrs['href']
        url = urljoin(BASE_URL, link)
        
        # Scrape each missed connection's page.
        scrape_missed_connection(url)


def scrape_missed_connection(url):
    """ Extract information from a deputy's page. """

    # Build the full URL for each deputy; download & parse it.
    response = requests.get(url)

    # Parse HTML
    soup = BeautifulSoup(response.content)

    # Extract the actual contents of some HTML elements:
    data = {
        'source_url': url,
        'subject': soup.find('h2', {'class':'postingtitle'}).text.strip(),
        'body': soup.find('section', {'id':'postingbody'}).text.strip(),
        'email': soup.find('a', {'class':'replylink'}).text.strip(),
        'datetime': soup.find('time').attrs['datetime']
    }
    
    # Print the url
    print "fetching " + url 
    
    # insert the data into the database
    table.upsert(data, ['source_url'])


if __name__ == '__main__':
    scrape_missed_connections()