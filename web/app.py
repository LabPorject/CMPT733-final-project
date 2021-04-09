from flask import Flask
import query_db_web as function

app = Flask(__name__)

@app.route('/')
def hello():
    columns = function.get_all_columns_name()
    return str(columns)
