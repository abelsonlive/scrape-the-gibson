# Scraping Workshop for NYU Gov 3.0 Skill-Share

These code snippets are the core of a scraping workshop for the NYU Gov 3.0 Skill-Share. It's addressed at people who have already done a bit of coding but want to explore scraping in `python` in more depth.  The workshop will be much easier if you have a Mac or Linux-based computer.


## Dependencies

1. Download repo: https://github.com/abelsonlive/nyu-skill-share-scraping

2. Install dependencies
  * If you don't have pip installed, type:
  ```
  sudo easy_install pip
  ```
  * change directories
  ```
  cd nyu-skill-share-scraping
  ````
  * now run:
  ```
  sudo pip install -r requirements.txt
  ```

## Topics

### Introduction 

* Getting started with Scraping in Python using [requests](http://docs.python-requests.org/en/latest/)
* Exploring HTML documents and extracting the data, with [BeautifulSoup](http://lxml.de/parsing.html)
* Saving scraped data to a database with [dataset](http://dataset.rtfd.org/)


### Advanced

* Thinking about ETL (Extract, Transform, Load)
* Keep your source data around.
* Running multiple requests in parallel to scrape faster
    * [Thready](https//github.com/pudo/thready)
* Regular Expressions to Extract More Data
* Programmatic crawling of entire sites.


## Links

There are plenty of existing resources on scraping. A few links:

* Paul Bradshaw's [Scraping for Journalists](https://leanpub.com/scrapingforjournalists), excellent for non-coders.
* [School of Data Handbook Recipes](http://schoolofdata.org/handbook/recipes/)
* [ScraperWiki (Classic) Docs](https://classic.scraperwiki.com/docs/python/), moving to [GitHub](https://github.com/frabcus/code-scraper-in-browser-tool/wiki)

