from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import pandas as pd

df = pd.read_csv('./pred_input.csv')
df = df.rename(columns={'imdb_avgRating': 'target'})
X,y = df.drop(['target'],axis=1), df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y)
print("start training")
tpot = TPOTRegressor(generations=25, population_size=25,subsample=0.7,max_time_mins=120,cv=3,periodic_checkpoint_folder='./m',memory='auto',warm_start=True,early_stop = 5,n_jobs=-1,verbosity=2,random_state=42)
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))
tpot.export('tpot_pipeline.py')