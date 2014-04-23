import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin
from thready import threaded
import dataset
import os
from hashlib import sha1

# A list of missed connections in New York
BASE_URL = 'http://newyork.craigslist.org/'

# connect to our database
db = dataset.connect('sqlite:///missed_connections.db')

# a directory for caching file's we've already downloaded
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')

def url_to_filename(url):
    """ Make a URL into a file name, using SHA1 hashes. """

    # use a sha1 hash to convert the url into a unique filename
    hash_file = sha1(url).hexdigest() + '.html'
    return os.path.join(CACHE_DIR, hash_file)


def store_local(url, content):
    """ Save a local copy of the file. """

    # If the cache directory does not exist, make one.
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Save to disk.
    local_path = url_to_filename(url)
    with open(local_path, 'wb') as f:
        f.write(content)


def load_local(url):
    """ Read a local copy of a URL. """
    local_path = url_to_filename(url)
    if not os.path.exists(local_path):
        return None

    with open(local_path, 'rb') as f:
        return f.read()


def get_content(url):
    """ Wrap requests.get() """
    content = load_local(url)
    if content is None:
        response = requests.get(url)
        content = response.content
        store_local(url, content)
    return content


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

    # create an empty list of urls to scrape 
    urls = []
    for missed_connection in missed_connections:
        
        # for each span list, find the "a" tag which 
        # represents the link to the missed connection page.

        link = missed_connection.find('a').attrs['href']
        
        # join this relative link with the 
        # BASE_URL to create an absolute link

        url = urljoin(BASE_URL, link)
        
        # iteratively populate this list 
        urls.append(url)


    # download and parse these missed connections using
    # multiple threads
    threaded(urls, scrape_missed_connection, num_threads=10)

def scrape_missed_connection(url):
    """ Extract information from a missed connections's page. """

    # log the url we're scraping
    print "scraping %s ..." % url

    # retrieve the missed connection with requests

    response = get_content(url)

    # Parse the html of the missed connection post

    soup = BeautifulSoup(response.content)

    # Extract the actual contents of some HTML elements:

    # here were using BeautifulSoup's `text` method for retrieving
    # the plain text within each HTML element.

    data = {
        'source_url': url,
        'subject': soup.find('h2', {'class':'postingtitle'}).text.strip(),
        'body': soup.find('section', {'id':'postingbody'}).text.strip(),
        'datetime': soup.find('time').attrs['datetime']
    }

    # Upsert the data into our database 
    db['posts'].upsert(data, ['source_url'])


if __name__ == '__main__':
    scrape_missed_connections()
