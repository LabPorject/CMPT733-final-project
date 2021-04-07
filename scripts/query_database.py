import pandas as pd
import json
import numpy as np
import pymongo
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client.aoligei
all_collection = db.all_movies
reviews = db.reviews
movielens_collection = db.movielens_movies
reviewlens_collection = db.movielens_reviews

# Note: movies that had reference from both imdb and tmdb
# Note: _id refers to IMDB id


def get_combined(release_year_cutoff=None, drop_lst=None, sample_size=None):
    pipeline = []
    pipeline.append({ '$match': { 'tmdb_id': { '$exists': 1 } } })
    
    if release_year_cutoff:
        if type(release_year_cutoff) != int:
            print('release_year need to be int')
            return -1
        else:
            pipeline.append( {'$addFields':{'release_year_int':{ '$toInt':"$release_year"}}} )
            pipeline.append( { '$match': { 'release_year_int': { '$gte': release_year_cutoff } } } )
    
    if drop_lst:
        if type(drop_lst) != list:
            print('drop need to be list')
            return -1
        else:
            it = iter(drop_lst)
            res_dct = dict(zip(it, [0]*len(drop_lst)))
            pipeline.append( { '$project': res_dct } )
            
    if sample_size:
        if type(sample_size) != int:
            print('sample_size need to be int')
            return -1
        else:
            pipeline.append( { '$limit' : sample_size } )    
            
    cursor = all_collection.aggregate(pipeline)
    df = pd.DataFrame(cursor)
    df['release_year'] = df['release_year'].astype(float)
    return df


# Note: _id refers to IMDB id
def get_reviews():
    cursor = reviews.find()
    return pd.DataFrame(cursor)

# Note: _id refers to IMDB id
def get_movieLens():
    cursor = movielens_collection.find()
    return pd.DataFrame(cursor)

def get_movieLens_reviews():
    cursor = reviewlens_collection.find({}, {'_id': 0})
    df = pd.DataFrame(cursor)
    return df

def get_all_columns_name():
    return ['_id',
     'primaryTitle',
     'originalTitle',
     'isAdult',
     'release_year',
     'release_date',
     'runtimeMinutes',
     'genres',
     'imdb_avgRating',
     'imdb_numVotes',
     'Directors',
     'casts',
     'tmdb_id',
     'poster_path',
     'original_language',
     'popularity',
     'budget',
     'revenue',
     'status',
     'tagline',
     'overview',
     'company_name',
     'keywords_name',
     'num_of_cast',
     'top_10_cast_popularity_mean',
     'top_10_cast_popularity',
     'num_of_crew',
     'top_10_crew_popularity_mean',
     'crews',
     'top_10_crew_popularity',
     'tmdb_avgRating',
     'tmdb_numVotes',
     'Writers',
     'homepage',
     'belongs_to_collection']

