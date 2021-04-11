from flask import Flask,render_template, request
import pandas as pd
import web_util as wu
import query_db_web as qdw
import copy
from flask import current_app
import ast
app = Flask(__name__)


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
        y_pred = current_app.rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        return render_template('random_rating.html',content=content)

@app.route('/<rdn>')
def randomRatingPage(rdn):
    if rdn == 'rdnrating':
        content = qdw.low_rating_random_movie()
        # print(content)
        wu.str_to_list(content)
        y_pred = current_app.rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        content['Directors'] = [d for d in content['Directors'] if d != 'None']
        return render_template('random_rating.html',content=content)
    elif rdn == 'goodlist':
        # content = {}
        content = qdw.high_rating_random_movie()
        wu.str_to_list(content)
        y_pred = current_app.rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        return render_template('random_rating.html',content=content)
    else:
        return """ <h1>Route Not Found</h1> """

if __name__ == "__main__":
    with app.app_context():
        current_app.rating_pred = qdw.get_model('rating',Description='Random Forest v2')
    app.run(host='localhost', port=5000,debug=True)
