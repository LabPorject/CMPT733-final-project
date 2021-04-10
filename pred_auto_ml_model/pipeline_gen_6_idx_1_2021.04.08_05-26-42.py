import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import MaxAbsScaler
from sklearn.svm import LinearSVR
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive
from sklearn.metrics import r2_score
import query_database as qd
import pickle
# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('./pred_input.csv',  dtype=np.float64)
tpot_data = tpot_data.rename(columns={'imdb_avgRating': 'target'})
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: -0.7848368988865041
exported_pipeline = make_pipeline(
    MaxAbsScaler(),
    StackingEstimator(estimator=LinearSVR(C=5.0, dual=True, epsilon=0.1, loss="epsilon_insensitive", tol=0.0001)),
    RandomForestRegressor(bootstrap=True, max_features=0.25, min_samples_leaf=17, min_samples_split=11, n_estimators=100)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
filename = 'random_forest_model_auto.pkl'
pickle.dump(exported_pipeline, open(filename, 'wb'))
print(r2_score(testing_target, results))

qd.store_model(pickle.dumps(filename), False, "Auto ML Predictor")