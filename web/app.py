from flask import Flask,render_template
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

@app.route('/recommend')
def recommendPage():
    return render_template('recommend.html')

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
