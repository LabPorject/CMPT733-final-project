import pandas as pd
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
import pickle
import gridfs

# client = MongoClient('ec2-107-20-117-240.compute-1.amazonaws.com', 27017)
client = MongoClient('127.0.0.1', 27017)

db = client.aoligei
all_collection = db.all_movies
reviews = db.reviews
movielens_collection = db.movielens_movies
reviewlens_collection = db.movielens_reviews
trained_models = db.ml_models
ml_models = gridfs.GridFS(db)


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

#model_type = "context", "collab", "rating"
def store_model(trained_model, model_type, note=None):
    if type(trained_model) != bytes:
        print('trained model needs to be in bytes')
        return -1

    name_dict = {"context": "Context-based Recommendation System"
    , "collab": "Collaborative Recommendation System"
    , "rating": "New Film Rating Prediction"}

    if model_type not in name_dict:
        print('model_type = "context", "collab" OR "rating"')
        return -1

    result = ml_models.put(
            trained_model,
            model_type=name_dict[model_type],
            Upload_time=datetime.now(),
            Description=note
        )
    print(result)


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


def get_poster_path(tmdb_id):
    if type(tmdb_id) != int:
        print('type error')
        return -1
    c = all_collection.aggregate([
        { '$project': {'_id':1,'tmdb_id':1, 'poster_path':1 } },
        { '$match': { 'tmdb_id': { '$exists': 1 } } },
        { '$match': { 'tmdb_id': tmdb_id } }
    ])
    returned_doc = list(c)[0]
    if 'poster_path' in returned_doc:
        return returned_doc['poster_path']
    else:
        return None

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

