import pandas as pd
import json
import numpy as np
import pymongo
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client.aoligei
imdb_collection = db.imdb_movies
tmdb_collection = db.tmdb_movies
all_collection = db.all_movies
reviews = db.reviews

def get_imdb():
    cursor = imdb_collection.find()
    return pd.DataFrame(cursor)


def get_tmdb():
    cursor = tmdb_collection.find()
    return pd.DataFrame(cursor)


def get_reviews():
    cursor = reviews.find()
    return pd.DataFrame(cursor)


# Note: movies that had reference from both imdb and tmdb
def get_combined():
    cursor = all_collection.find({ 'tmdb_id': { '$exists': 1 } })
    return pd.DataFrame(cursor)