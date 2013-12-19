import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin

# The base url for craigslist in New York
BASE_URL = 'http://newyork.craigslist.org/'

def scrape_missed_connections():
    """ Scrape all the missed connections from a list """
    
    # Download the list of missed connections

    # here were using requests, 
    # a python library for accessing the web

    # we add "mis/" to the url to tell requests
    # to get the missed connections 
    # on newyork.craigslist.org

    response = requests.get(BASE_URL + "mis/")

    # parse HTML using Beautiful Soup
    # this returns a `soup` object which
    # gives us convenience methods for parsing html

    soup = BeautifulSoup(response.content)

    # find all the posts in the page.

    # here we're telling BeautifulSoup to get us every
    # span tag that has a class that equals pl

    # these tags might look something like this:
    # <span class='pl'> {content} </span>

    missed_connections = soup.find_all('span', {'class':'pl'})

    # Get all the links to missed connection pages:
    for missed_connection in missed_connections:
        
        # for each span list, find the "a" tag which 
        # represents the link to the missed connection page.

        link = missed_connection.find('a').attrs['href']
        
        # join this relative link with the 
        # BASE_URL to create an absolute link

        url = urljoin(BASE_URL, link)
        
        # pass this url to a function (defined below) to scrape 
        # info about that missed connection

        scrape_missed_connection(url)

def scrape_missed_connection(url):
    """ Extract information from a missed connections's page. """

    # retrieve the missed connection with requests

    response = requests.get(url)

    # Parse the html of the missed connection post

    soup = BeautifulSoup(response.content)

    # Extract the actual contents of some HTML elements:

    # here were using BeautifulSoup's `text` method for retrieving
    # the plain text within each HTML element.

    # see and example of what this page looks like here:

    data = {
        'source_url': url,
        'subject': soup.find('h2', {'class':'postingtitle'}).text.strip(),
        'body': soup.find('section', {'id':'postingbody'}).text.strip(),
        'datetime': soup.find('time').attrs['datetime']
    }

    # Print it prettily. 
    pprint(data)

if __name__ == '__main__':
    scrape_missed_connections()