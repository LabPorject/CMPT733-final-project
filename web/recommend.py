import pandas as pd
import os
import sys
module_path = os.path.abspath(os.path.join('../scripts'))
if module_path not in sys.path:
    sys.path.append(module_path)
from similarity import SimilarityPredictions
from query_db_web import get_all_movies
def get_recs_with_model(movie_id, sim_model):
    #get similar movies
    df = pd.DataFrame(get_all_movies())
    output = sim_model.predict_similar_items(seed_item=movie_id, n=15)
    similar_movies = pd.DataFrame(output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df = pd.merge(df, similar_movies, left_index=True, right_index=True)
    sim_df.sort_values('similarity_score', ascending=False, inplace=True)
    return sim_df.iloc[1:]

def get_recs(movie_id, embeddings):
    #get similar movies
    df = pd.DataFrame(get_all_movies())
    sim_model = SimilarityPredictions(embeddings, similarity_metric="cosine")
    output = sim_model.predict_similar_items(seed_item=movie_id, n=15)
    similar_movies = pd.DataFrame(output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df = pd.merge(df, similar_movies, left_index=True, right_index=True)
    sim_df.sort_values('similarity_score', ascending=False, inplace=True)
    return sim_df.iloc[1:]