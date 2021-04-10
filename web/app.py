from flask import Flask,render_template
import pandas as pd
import web_util as wu
import query_db_web as qd
import copy
from flask import current_app
app = Flask(__name__)


@app.route('/')
def mainPage():
    return render_template('home.html')

@app.route('/rating')
def predModelPage():
    return render_template('pred_model.html')

@app.route('/customize')
def diyRatingPage():
    return render_template('random_rating.html')

@app.route('/<rdn>')
def randomRatingPage(rdn):
    # model = qd.get_model('rating',Description='Random Forest v2')
    # k = wu.processing_input(copy.deepcopy(content))
    if rdn == 'rdnrating':
        content = wu.random_input(False)
        y_pred = current_app.rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        content['Directors'] = [d for d in content['Directors'] if d != 'None']
        return render_template('random_rating.html',content=content)
    elif rdn == 'goodlist':
        content = wu.random_input(True)
        y_pred = current_app.rating_pred.predict(wu.processing_input(copy.deepcopy(content)))
        content['rating'] = y_pred
        return render_template('random_rating.html',content=content)
    else:
        return """ <h1>Route Not Found</h1> """

if __name__ == "__main__":
    with app.app_context():
        current_app.rating_pred = qd.get_model('rating',Description='Random Forest v2')
    app.run(host='localhost', port=5000,debug=True)
