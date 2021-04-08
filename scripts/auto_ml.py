import autosklearn.regression
import sklearn.metrics
import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv('./pred_input.csv')
X,y = df.drop(['imdb_avgRating'],axis=1), df['imdb_avgRating']
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

automl = autosklearn.regression.AutoSklearnRegressor(resampling_strategy='cv')
automl.fit(X_train, y_train)
print(automl.show_models())
predictions = automl.predict(X_valid)
print("R2 score:", sklearn.metrics.r2_score(y_valid, predictions))
Pkl_Filename = "auto_sklearn.pkl"
with open(Pkl_Filename, 'wb') as file:  
    pickle.dump(automl, file)
with open(Pkl_Filename, 'rb') as file:  
    Pickled_LR_Model = pickle.load(file)
predictions = Pickled_LR_Model.predict(X_valid)
print("R2 score:", sklearn.metrics.r2_score(y_valid, predictions))