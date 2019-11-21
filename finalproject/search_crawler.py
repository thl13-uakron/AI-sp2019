# Written by Thomas Li
# Artificial Intelligence and Heuristics 460
# Fall 2019

# This module contains methods for retrieving and processing information that
# can be obtaining from putting a certain term through a search engine.

# from serpapi.google_search_results import GoogleSearchResults
import re
import urllib.request
from googlesearch import search
from bs4 import BeautifulSoup

"""
SERP API approach requires paying money for an account in order to run 
automated searches on a large-enough scale for this project

google_client = GoogleSearchResults({})

def get_google_results(title):
    global google_client
    google_client.params_dict["p"] = title
    return google_client.get_dict()
"""

# filter out certain webpages using regular expressions
url_filter = r"wikipedia|youtube"

# retrieve the text content of a webpage given a url
def get_url_content(url):
    try:
        # retrieve page
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        
        # filter out tags, scripts, headings, and styles
        soup = BeautifulSoup(response.read().decode("utf8"), "lxml").body
        [script.decompose() for script in soup.find_all("script")]
        [style.decompose() for style in soup.find_all("style")]
        
        return soup.get_text()
    
    except:
        return ""

# get an iterable of urls returned from searching a term on google
def get_google_result_urls(title, hits):
    urls = search(title, stop=hits)
    return urls

# get the contents associated with each returned url
def get_google_result_contents(title, hits=20):
    urls = get_google_result_urls(title, hits)
    return {url : get_url_content(url) for url in urls
            if re.search(url_filter, url) == None}