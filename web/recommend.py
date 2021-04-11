import pickle
import pandas as pd
import os
import sys
from similarity import SimilarityPredictions

def get_recs_with_model(movie_id, sim_model):
    #get similar movies
    df = pd.read_csv('../all_movies_poster.csv')
    output = sim_model.predict_similar_items(seed_item=movie_id, n=15)
    similar_movies = pd.DataFrame(output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df = pd.merge(df, similar_movies, left_index=True, right_index=True)
    sim_df.sort_values('similarity_score', ascending=False, inplace=True)
    return sim_df

def get_recs(movie_id, embeddings):
    #get similar movies
    df = pd.read_csv('../all_movies_poster.csv')
    sim_model = SimilarityPredictions(embeddings, similarity_metric="cosine")
    output = sim_model.predict_similar_items(seed_item=movie_id, n=15)
    similar_movies = pd.DataFrame(output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df = pd.merge(df, similar_movies, left_index=True, right_index=True)
    sim_df.sort_values('similarity_score', ascending=False, inplace=True)
    return sim_df.iloc[1:]