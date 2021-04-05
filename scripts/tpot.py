from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

df = pd.read_csv('./pred_input.csv')
X,y = df.drop(['imdb_avgRating'],axis=1), df['imdb_avgRating']
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42)
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))
tpot.export('tpot_pipeline.py')

Pkl_Filename = "auto_tpot.pkl"
with open(Pkl_Filename, 'wb') as file:  
    pickle.dump(tpot, file)