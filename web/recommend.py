import pandas as pd
import os
import sys
from similarity import SimilarityPredictions
from query_db_web import get_all_movies
# df = pd.DataFrame(get_all_movies())
df = pd.DataFrame(get_all_movies())
def get_recs_with_model(movie_id, sim_model):
    #get similar movies
    output = sim_model.predict_similar_items(seed_item=movie_id, n=21)
    similar_movies = pd.DataFrame(output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df = pd.merge(df, similar_movies, left_index=True, right_index=True)
    sim_df.sort_values('similarity_score', ascending=False, inplace=True)
    return sim_df.iloc[1:]

def get_recs(movie_id, embeddings):
    #get similar movies
    sim_model = SimilarityPredictions(embeddings, similarity_metric="cosine")
    output = sim_model.predict_similar_items(seed_item=movie_id, n=15)
    similar_movies = pd.DataFrame(output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df = pd.merge(df, similar_movies, left_index=True, right_index=True)
    sim_df.sort_values('similarity_score', ascending=False, inplace=True)
    return sim_df.iloc[1:]

def get_ensemble_recs_with_model(movie_id, model_1, model_2):
    #get similar movies from content 1
    cont_output = model_1.predict_similar_items(seed_item=movie_id, n=21639)
    similar_movies = pd.DataFrame(cont_output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df_cont = similar_movies.rename(index=str, columns={"similarity_score": "similarity_score_1"})
    #get similar movies from content 2
    coll_output = model_2.predict_similar_items(seed_item=movie_id, n=21639)
    similar_movies = pd.DataFrame(coll_output)
    similar_movies.set_index('item_id', inplace=True)
    sim_df_coll = similar_movies.rename(index=str, columns={"similarity_score": "similarity_score_2"})
    #ensemble results
    sim_df_avg = pd.merge(sim_df_coll, pd.DataFrame(sim_df_cont['similarity_score_1']), left_index=True, right_index=True)
    sim_df_avg['average_similarity_score'] = (sim_df_avg['similarity_score_1'] + sim_df_avg['similarity_score_2'])/2
    sim_df_avg.drop("similarity_score_1", axis=1, inplace=True)
    sim_df_avg.drop("similarity_score_2", axis=1, inplace=True)
    sim_df_avg.reset_index(inplace=True)
    sim_df_avg['item_id']=sim_df_avg['item_id'].astype(int)
    sim_df_avg = df.merge(sim_df_avg, left_index=True, right_on='item_id')
    sim_df_avg.sort_values('average_similarity_score', ascending=False, inplace=True)
    sim_df_avg.drop("item_id", axis=1, inplace=True)
    sim_df_avg.reset_index(drop=True, inplace=True)
    return sim_df_avg.head(21).iloc[1:]