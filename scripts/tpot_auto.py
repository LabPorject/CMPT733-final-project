from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import pandas as pd

df = pd.read_csv('./pred_input.csv')
df = df.rename(columns={'imdb_avgRating': 'target'})
X,y = df.drop(['target'],axis=1), df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y)

tpot = TPOTRegressor()
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))
tpot.export('tpot_pipeline.py')

# Pkl_Filename = "auto_tpot.pkl"
# with open(Pkl_Filename, 'wb') as file:  
#     pickle.dump(tpot, file)