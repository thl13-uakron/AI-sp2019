# Written by Thomas Li
# Artificial Intelligence and Heuristics 460
# Fall 2019

# This module contains methods for retrieving and processing content from
# Wikipedia, including article text and category information

import urllib.request
from bs4 import BeautifulSoup
from mediawiki import MediaWiki

# data representation for individual articles
# current approach using tools provided by the pymediawiki module
wikipedia = MediaWiki()
def get_article(topic_name):
    page = wikipedia.page(topic_name)
    return {"title" : page.title,
            "summary" : page.summary,
            "categories" : page.categories}
"""
older approach involving scraping pages corresponding to articles and
attempting to parse the full HTML

class Article:
    # full page contents
    html = {}

    # individual components
    # raw article text (by section)
    article_text = {}
    # article name
    topic_name = ""
    # infobox contents
    infobox = {}
    # categories listed on page
    categories = []

    # constructor to retrieve contents of a given article topic using a spider
    def __init__(self, topic_name):
        self.topic_name = topic_name
        
        # form article url, request page, and get response
        url = "https://en.wikipedia.org/wiki/" + topic_name.replace(" ", "_")
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        
        # get full page content in parseable form
        self.html = response.read().decode("utf8")
        self.html = BeautifulSoup(self.html, "lxml")

    # accessors for retrieving components of article
    # article name
    def get_topic_name(self):
        return self.topic_name
    # full html
    def get_html(self):
        return self.html
    # article contents for all sections
    def get_article_text(self):
        return self.article_text
    # intro section contents
    def get_intro_text(self):
        return self.article_text
    # infobox contents
    def get_infobox(self):
        try:
            parent_element = self.html.find("table", {"class":"infobox vevent"}).tbody
            return parent_element
        except:
            return {}
    # categories listed on pages
    def get_categories(self):
        parent_element = self.html.find("div", id="mw-normal-catlinks").ul
        return [category for category_item in parent_element.find_all("li")
                for category in category_item.a.children]
        
    # return the article in object form for database storage
    def get_object(self):
        return {"html":self.html}
"""
# get a list of the titles of each good article
def get_good_article_titles():
    return
# get an iterable that yields the contents of each good article
def get_good_articles():
    yield 
    
# get a list of the titles of each featured article
def get_featured_article_titles():
    url = "https://en.wikipedia.org/wiki/Wikipedia:Featured_articles"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    
    html = response.read().decode("utf8")
    parent_element = BeautifulSoup(html).find("div", {"class":"hlist", "style":"margin: 1px; vertical-align:top; padding:1em 1em 1em 1em; border:1px solid #A3BFB1; background-color:#F1F6FB"})
    return [e.get_text() for e in parent_element.find_all("li")]
# get an iterable that yields the contents of each featured article
def get_featured_articles():
    for title in get_featured_article_titles():
        yield get_article(title)
    
# test the functions in this module
def test():
    print(get_article("Youngstown, Ohio"))
    print(get_article("Python (Programming Language)"))
    print(get_featured_article_titles())
    articles = get_featured_articles()
    i = 0
    for a in articles:
        print(a)
        i += 1
        if i > 5:
            break
    