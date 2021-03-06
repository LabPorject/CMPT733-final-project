from flask import Flask,render_template, url_for, redirect, current_app, request
from query_db_web import get_random_movies_with_poster, get_model
import json
from recommend import get_recs_with_model, get_hybrid_recs_with_model, get_ensemble_recs_with_model
import pickle
import pandas as pd
import web_util as wu
import query_db_web as qdw
import copy
from similarity import SimilarityPredictions
app = Flask(__name__)
content_embeddings_v3 = get_model(model_type="context", Description="Context-based: Chao Zhang Version 3")
content_embeddings_v3 = pd.DataFrame(content_embeddings_v3)
model_content_v3 = SimilarityPredictions(content_embeddings_v3, similarity_metric="cosine")

content_embeddings_v1 = get_model(model_type="context", Description="Context-based: Chao Zhang Version 1")
content_embeddings_v1 = pd.DataFrame(content_embeddings_v1)
model_content_v1 = SimilarityPredictions(content_embeddings_v1, similarity_metric="cosine")

collaborative_embeddings_v2 = get_model(model_type="collab", Description="Collaborative filtering: Chao Zhang Version 2")
collaborative_embeddings_v2 = pd.DataFrame(collaborative_embeddings_v2)
model_collab_v2 = SimilarityPredictions(collaborative_embeddings_v2, similarity_metric="cosine")

rating_pred = qdw.get_model('rating',Description='Random Forest v2')


@app.route('/')
def mainPage():
    return render_template('home.html')

@app.route('/rating')
def predModelPage():
    return render_template('pred_model.html')

@app.route('/customize', methods=['GET', 'POST'])
def diyRatingPage():
    if request.method == 'GET':
        content = {}
        content['genres'] = qdw.get_maxxu_list('genres')
        content['belongs_to_collection'] = ['None'] + qdw.get_maxxu_list('belongs_to_collection')
        content['keywords_name'] = ['None'] + qdw.get_maxxu_list('keywords_name')
        return render_template('rating_form.html',content=content)
    elif request.method == 'POST':
        content = wu.processing_cus_input(request.form)
        y_pred = rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        return render_template('random_rating.html',content=content)

@app.route('/recommend')
def recommendPage():
    return render_template('recommend.html', movies=get_random_movies_with_poster(20))

@app.route('/recommend_collab')
def recommendPageCollab():
    return render_template('recommend_collab.html', movies=get_random_movies_with_poster(20))

@app.route('/recommend_hybrid')
def recommendPageHybrid():
    return render_template('recommend_hybrid.html', movies=get_random_movies_with_poster(20))

@app.route('/update')
def update_list():
    clicked_movieId = request.args.get('movieId')
    return redirect(url_for('recommend', movie_id=clicked_movieId))

@app.route('/update_collab')
def update_list_collab():
    clicked_movieId = request.args.get('movieId')
    return redirect(url_for('recommend_collab', movie_id=clicked_movieId))

@app.route('/update_hybrid')
def update_list_hybrid():
    clicked_movieId = request.args.get('movieId')
    return redirect(url_for('recommend_hybrid', movie_id=clicked_movieId))

@app.route('/recommend/<movie_id>', methods=['GET'])
def recommend(movie_id):
    df = get_ensemble_recs_with_model(int(movie_id), model_content_v1, model_content_v3)
    return render_template('recommend.html', movies=list(df.to_dict('index').values()))

@app.route('/recommend_collab/<movie_id>', methods=['GET'])
def recommend_collab(movie_id):
    df = get_recs_with_model(int(movie_id), model_collab_v2)
    return render_template('recommend_collab.html', movies=list(df.to_dict('index').values()))

@app.route('/recommend_hybrid/<movie_id>', methods=['GET'])
def recommend_hybrid(movie_id):
    df = get_hybrid_recs_with_model(int(movie_id), model_content_v3, model_collab_v2)
    return render_template('recommend_hybrid.html', movies=list(df.to_dict('index').values()))

@app.route('/test')
def user():
    return render_template('test.html', movies=get_random_movies_with_poster(10))

@app.route('/<rdn>')
def randomRatingPage(rdn):
    if rdn == 'rdnrating':
        content = qdw.low_rating_random_movie()
        # print(content)
        wu.str_to_list(content)
        y_pred = rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        content['Directors'] = [d for d in content['Directors'] if d != 'None']
        return render_template('random_rating.html',content=content)
    elif rdn == 'goodlist':
        # content = {}
        content = qdw.high_rating_random_movie()
        wu.str_to_list(content)
        y_pred = rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        return render_template('random_rating.html',content=content)
    else:
        return """ <h1>Route Not Found</h1> """

if __name__ == "__main__":
    # with app.app_context():
    #     current_app.rating_pred = qdw.get_model('rating',Description='Random Forest v2')
    app.run(host='localhost', port=5000,debug=True)
