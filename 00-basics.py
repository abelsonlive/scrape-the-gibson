import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin


# A list of missed connections in New York
BASE_URL = 'http://newyork.craigslist.org/'


def scrape_missed_connections():
    """ Scrape all the missed connections from a list """
    
    # Download the list.
    response = requests.get(BASE_URL + "mis/")

    # Parse HTML
    soup = BeautifulSoup(response.content)

    # Get all the links to missed connections:
    for missed_connection in soup.find_all('span', {'class':'pl'}):
        
        # extract link path
        link = missed_connection.find('a').attrs['href']
        
        # join with base url
        url = urljoin(BASE_URL, link)
        
        # pass missed connection url to a function to scrape info about that missed connection below
        scrape_missed_connection(url)


def scrape_missed_connection(url):
    """ Extract information from a missed connections's page. """

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

    # Print it. 
    pprint(data)


if __name__ == '__main__':
    scrape_missed_connections()
