import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin
import dataset
import os
from hashlib import sha1

#############
# Thready is a very simple code snippet: 
#   http://github.com/pudo/thready
#############
from thready import threaded

# A list of missed connections in New York
BASE_URL = 'http://newyork.craigslist.org/'

# a directory for cacheing file's we've already downloaded
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')

# connect to our database
database = dataset.connect('sqlite:///missed_connections.db')

# get a table
table = database['missed_connections']


def url_to_filename(url):
    """ Make a URL into a file name, using SHA1 hashes. """
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
    """ Scrape all the deputies from the list """
    
    # Download the list.
    content = get_content(BASE_URL + "mis/")

    # Parse HTML
    soup = BeautifulSoup(content)

    # Get all the links to missed connections:
    urls = []
    for missed_connection in soup.find_all('span', {'class':'pl'}):
        
        link = missed_connection.find('a').attrs['href']
        url = urljoin(BASE_URL, link)
        urls.append(url)

    threaded(urls, scrape_missed_connection, num_threads=10)

def scrape_missed_connection(url):
    """ Extract information from a deputy's page. """

    # Build the full URL for each deputy; download & parse it.
    content = get_content(url)

    # Parse HTML
    soup = BeautifulSoup(content)

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