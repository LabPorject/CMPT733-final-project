from query_db_web import get_random_movies_with_poster
from flask import Flask,render_template, url_for, redirect
from flask import request
import json
from recommend import get_recs_with_model, get_recs
import pickle
import pandas as pd
app = Flask(__name__)
# with open('../model_content_v3.pkl', 'rb') as model:
#     model_content_v3 = pickle.load(model)

content_embeddings_v3 = pd.read_pickle("../final_models/autoencoder_embeddings-v3.pkl")
content_embeddings_v3 = pd.DataFrame(content_embeddings_v3)
@app.route('/')
def mainPage():
    return render_template('home.html')

@app.route('/rating')
def predModelPage():
    return render_template('pred_model.html')

@app.route('/customize')
def diyRatingPage():
    return render_template('random_rating.html')

@app.route('/recommend')
def recommendPage():
    return render_template('recommend.html', movies=get_random_movies_with_poster(10))


@app.route('/update')
def update_list():
    clicked_movieId = request.args.get('movieId')
    return redirect(url_for('recommend', movie_id=clicked_movieId))

@app.route('/recommend/<movie_id>', methods=['GET'])
def recommend(movie_id):
    df = get_recs(int(movie_id), content_embeddings_v3)
    return render_template('recommend.html', movies=list(df.to_dict('index').values()))
    # df = get_recs_with_model(int(movie_id), model_content_v3)
    # return render_template('recommend.html', movies=list(df.to_dict('index').values()))

@app.route('/test')
def user():
    return render_template('test.html', movies=get_random_movies_with_poster(10))

@app.route('/<rdn>')
def randomRatingPage(rdn):
    if rdn == 'rdnrating':
        return render_template('random_rating.html')
    elif rdn == 'goodlist':
        return render_template('random_rating.html')
    else:
        return """ <h1>Route Not Found</h1> """

if __name__ == "__main__":
    app.run(host='localhost', port=5000,debug=True)
