import pandas as pd
import json
import numpy as np
import pymongo
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client.aoligei
imdb_collection = db.imdb_movies

movies = pd.read_csv('./raw_data/IMDB/title.basics.tsv', sep='\t')

movies = movies[movies['titleType']=='movie'].reset_index()

movies = movies.drop(['index', 'titleType', 'endYear'], axis=1)
movies = movies.replace('\\N', np.nan)

movies['genres'] = movies.genres.str.split(',')

ratings = pd.read_csv('./raw_data/IMDB/title.ratings.tsv', sep='\t')

movies_ratings = movies.merge(ratings, how='left', left_on='tconst', right_on='imdb_id')

movies_ratings = movies_ratings.set_index('tconst')

movies_ratings = movies_ratings.drop(['imdb_id'], axis=1)

principles = pd.read_csv('./raw_data/IMDB/title.principals.tsv', sep='\t', usecols=['tconst','nconst', 'category'])

principles = principles.replace('\\N', np.nan)

names = pd.read_csv('./raw_data/IMDB/name.basics.tsv', sep='\t', usecols=['nconst','primaryName'])

principles_withname = principles.merge(names, on='nconst').drop(['nconst'], axis=1)

directors = principles_withname[principles_withname['category'] == 'director']

directors = directors.set_index('tconst')

helper = movies_ratings.merge(directors, how='left', left_index=True, right_index=True)

director_list = helper.groupby('tconst').primaryName.apply(list).reset_index()

director_list = director_list.set_index('tconst')

movies_dir = movies_ratings.merge(director_list, how='left', left_index=True, right_index=True)

movies_dir = movies_dir.rename(columns={"primaryName": "Directors"})

writers = principles_withname[principles_withname['category'] == 'writer']

writers = writers.set_index('tconst')

helper_w = movies_ratings.merge(writers, how='left', left_index=True, right_index=True)

writer_list = helper_w.groupby('tconst').primaryName.apply(list).reset_index().set_index('tconst')

movies_wri = movies_dir.merge(writer_list, how='left', left_index=True, right_index=True).rename(columns={"primaryName": "Writers"})

cast = principles_withname[(principles_withname['category'] == 'actor') | (principles_withname['category'] == 'actress' )]

cast = cast.set_index('tconst')

helper_c = movies_ratings.merge(cast, how='left', left_index=True, right_index=True)

cast_list = helper_c.groupby('tconst').primaryName.apply(list).reset_index().set_index('tconst')

movies_cast = movies_wri.merge(cast_list, how='left', left_index=True, right_index=True).rename(columns={"primaryName": "Casts"})

movies_cast = movies_cast.reset_index().rename(columns={"tconst": "_id"})

movies_cast['runtimeMinutes'] = movies_cast['runtimeMinutes'].astype(float)

clean_imdb = movies_cast.rename(columns={'startYear': 'release_year'
                                         , 'averageRating': 'imdb_avgRating'
                                         , 'numVotes': 'imdb_numVotes'
                                         , 'Casts': 'casts'})

movies_tojson = clean_imdb.to_json(orient="records")
result = json.loads(movies_tojson)

imdb_collection.insert_many(result)

imdb_keys = ['release_year','genres','imdb_avgRating','imdb_numVotes','Directors','Writers','casts','runtimeMinutes']

#remove null valued key-value pairs to save space
for key in imdb_keys:
    imdb_collection.update_many(
#         {key: None},
        { '$or': [ { key: None }, { key: '' }, { key: [] } ] },
        {'$unset': { key: ''}}   
    )














