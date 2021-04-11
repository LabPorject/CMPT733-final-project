import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
import pickle
import gridfs

# client = MongoClient('ec2-107-20-117-240.compute-1.amazonaws.com', 27017)

# client = MongoClient('127.0.0.1', 27017)
client = MongoClient('mongo', 27017)

db = client.aoligei
all_collection = db.all_movies
reviews = db.reviews
movielens_collection = db.movielens_movies
reviewlens_collection = db.movielens_reviews
trained_models = db.ml_models
ml_models = gridfs.GridFS(db)

recomm_testset = db.recomm_testset
pred_rating_random = db.pred_rating_testset


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


def get_random_movies(n):
    cursor = recomm_testset.aggregate([
        { '$project': {'_id': 0 } },
        { '$sample': { 'size': n } }
    ])
    return list(cursor)


def get_random_movies_with_poster(n):
    cursor = recomm_testset.aggregate([
        { '$project': {'_id': 0 } },
        { '$match': { 'poster_path': { '$exists': 1 } } },
        { '$sample': { 'size': n } }
    ])
    return list(cursor)


# return a python list
def high_rating_random_movie():
    cursor = pred_rating_random.aggregate([
        { '$project': {'_id': 0, 'index': 0 } },
        { '$match': { 'rating': 'low' } },
        { '$sample': { 'size': 1 } }
    ])
    _dict = list(cursor)[0]
    del _dict['rating']
    return _dict


# return a python list
def low_rating_random_movie():
    cursor = pred_rating_random.aggregate([
        { '$project': {'_id': 0, 'index': 0 } },
        { '$match': { 'rating': 'high' } },
        { '$sample': { 'size': 1 } }
    ])
    _dict = list(cursor)[0]
    del _dict['rating']
    return _dict


# return a python list
def get_maxxu_list(which):
    if which not in get_maxxu_all_lists_name():
        print('incorrect list name')
        return -1

    returned_dict = pred_rating_random.find({'pred_rating_lists' : 1}, { which : 1})[0]
    return list(returned_dict[which].values())[0]


def get_maxxu_all_lists_name():
    return ['high_casts', 'belongs_to_collection', 'low_crews', 'keywords_name', 'genres'
    , 'high_Writers', 'high_crews', 'high_Directors', 'low_Directors', 'low_casts', 'low_Writers']

def get_all_movies():
    cursor = recomm_testset.aggregate([
        { '$project': {'_id': 0 } }
    ])
    return list(cursor)

