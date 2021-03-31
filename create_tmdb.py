import pandas as pd
import json
import numpy as np
import pymongo
from pymongo import MongoClient
from scripts.tmdb_api import getInfoIMDB

client = MongoClient('127.0.0.1', 27017)
db = client.aoligei
imdb_collection = db.imdb_movies
tmdb_collection = db.tmdb_movies
reviews = db.reviews

imdb_cursor = imdb_collection.find({}, {'_id': 1})

count = 0

for p in imdb_cursor:
    
    if (count % 1000) == 0:
        print(count)
    count += 1

    try:
        info = getInfoIMDB(p['_id'])
        if info is not None:
            tmdb_collection.insert_one(json.loads(info[0]))
            reviews.insert_one(json.loads(info[1]))
    except:
        print(p['_id'])

        kill 16993