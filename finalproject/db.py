# Written by Thomas Li
# Artificial Intelligence and Heuristics 460
# Fall 2019

# This module contains methods for accessing and using the MongoDB server used
# to store the dataset for this project

# The initial insertion of the information was done through the shell as it
# only needed to occur once

from pymongo import MongoClient

# database url
connection_string = "127.0.0.1:27017"

# database connections
client = MongoClient(connection_string)
db = client.AI_sp2019_project

# collections
db_articles = db.articles # articles
db_search_results = db.search_results # results from googling article titles

# get article from db by title
def db_get_article(title):
    return db_articles.find_one({"title": title})