import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
import pickle
import gridfs

client = MongoClient('ec2-107-20-117-240.compute-1.amazonaws.com', 27017)
# client = MongoClient('127.0.0.1', 27017)

db = client.aoligei
all_collection = db.all_movies
reviews = db.reviews
movielens_collection = db.movielens_movies
reviewlens_collection = db.movielens_reviews
trained_models = db.ml_models
ml_models = gridfs.GridFS(db)



def get_model(model_type, Description=None):
    fsCollection = db.fs.files

    name_dict = {"context": "Context-based Recommendation System"
    , "collab": "Collaborative Recommendation System"
    , "rating": "New Film Rating Prediction"}

    if model_type not in name_dict:
        print('model_type = "context", "collab" OR "rating"')
        return -1

    if Description:
        returned_dict = fsCollection.find({"model_type": name_dict[model_type]
            , "Description": Description}).sort(  "uploadDate", -1  )[0]
    else:
        returned_dict = fsCollection.find({"model_type": name_dict[model_type]}) \
        .sort(  "uploadDate", -1  )[0]
    _id = returned_dict["_id"]
    out = ml_models.get(_id)
    returned_pickle = out.read()
    model = pickle.loads(returned_pickle)

    print('returned a ' + name_dict[model_type] + ' model, which was created at ' 
        + returned_dict['uploadDate'].strftime("%m/%d/%Y, %H:%M:%S"))
    print('Note on the model: ' + returned_dict['Description'])
    return model

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

