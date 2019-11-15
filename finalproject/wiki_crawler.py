# Written by Thomas Li
# Artificial Intelligence and Heuristics 460
# Fall 2019

# This module contains methods for retrieving and processing content from
# Wikipedia, including article text and category information

import urllib.request
from bs4 import BeautifulSoup

# get an iterable that yields every article in a list
def get_articles_in_list(list_name):
    yield  

# data representation for individual articles
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
        return self.infobox
    # categories (as listed on page)
    def get_categories(self):
        parent_element = self.html.find("div", id="mw-normal-catlinks").ul
        return parent_element
    # categories (including all super-categories)
    def get_all_categories(self):
        # recursively find each category that the current categories fall under
        # and append them to the list of categories to return
        return self.get_categories() + [super_category for category in self.categories 
                                  for super_category
                                  in Article("Category:" + category).get_all_categories()
                                  ]
        
    # return the article in object form for database storage
    def get_object(self):
        return
    
    

def test():
    a = Article("Python (programming language)")
    print(a.get_categories())