import pandas as pd
import json
import numpy as np
import pymongo
from pymongo import MongoClient
import difflib


def entity_res(list1, list2):
    for i in list2:
        if len(difflib.get_close_matches(i, list1, cutoff=0.7)) == 0:
               list1.append(i)
    return list1


def main():
    client = MongoClient('127.0.0.1', 27017)
    db = client.aoligei
    imdb_collection = db.imdb_movies
    tmdb_collection = db.tmdb_movies
    reviews = db.reviews

    imdb_keys = ['release_year','genres','imdb_avgRating','imdb_numVotes','Directors','Writers','casts','runtimeMinutes']

    #remove null valued key-value pairs to save space
    for key in imdb_keys:
        imdb_collection.update_many(
    #         {key: None},
            { '$or': [ { key: None }, { key: '' }, { key: [] } ] },
            {'$unset': { key: ''}}   
        )

    tmdb_keys = ['genres','vote_average','vote_count','poster_path','original_language','popularity','budget'
                 ,'revenue','status','tagline','homepage','belongs_to_collection','release_date'
                 ,'overview','originalTitle','runtimeMinutes','company_name','keywords_name','num_of_cast'
                 ,'top_10_cast_popularity_mean','casts','top_10_cast_popularity','num_of_crew','Writers'
                 ,'top_10_crew_popularity_mean','crews','top_10_crew_popularity','Directors']

    #remove null valued key-value pairs to save space
    for key in tmdb_keys:
        tmdb_collection.update_many(
    #         {key: None},
            { '$or': [ { key: None }, { key: '' }, { key: [] } ] },
            {'$unset': { key: ''}}   
        )

    tmdb_collection.update_many( {}, { '$rename': { "vote_average": "tmdb_avgRating" } } )
    tmdb_collection.update_many( {}, { '$rename': { "vote_count": "tmdb_numVotes" } } )

    #project out 'release_date': 0, 'primaryTitle': 0, 'originalTitle': 0, 'isAdult': 0
    tmdb_iterator = tmdb_collection.find({}, {'primaryTitle': 0, 'originalTitle': 0, 'isAdult': 0})

    for tmovie in tmdb_iterator:
        _id = tmovie['_id']
        if imdb_collection.find({'_id': _id}).count() == 0:
            break
        imovie = imdb_collection.find({'_id': _id})[0]
        try:
            for key in tmovie.keys():
                #always use the casts from tmdb for popularity feature that only tmdb has
                if key == 'casts':
                    imdb_collection.update_one({'_id': _id}
                                    , {'$set': {key: tmovie[key]}})
                elif key == 'Directors' and key in imovie:
                    imdb_collection.update_one({'_id': _id}
                                    , {'$set': { key: entity_res(imovie[key], [tmovie[key]]) }})
                elif key == 'genres' and key in imovie:
                    imdb_collection.update_one({'_id': _id}
                                    , {'$set': { key: entity_res(imovie[key], tmovie[key]) }})  
                elif key == 'Writers' and key in imovie:
                    imdb_collection.update_one({'_id': _id}
                                    , {'$set': { key: entity_res(imovie[key], tmovie[key]) }})  
                else:
                    imdb_collection.update_one( 
                        {'_id': _id, key:{ '$exists': 0 }}
                        , {'$set': {key: tmovie[key]}} )
        except:
            print(_id)

    #drop documents that does not have a review
    reviews.delete_many({'review': []})

    imdb_collection.rename('all_movies')

if __name__=='__main__':
    main()
