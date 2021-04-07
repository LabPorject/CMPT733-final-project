import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoLarsCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import Normalizer
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive
from sklearn.preprocessing import FunctionTransformer
from copy import copy
from sklearn.metrics import r2_score
# NOTE: Make sure that the outcome column is labeled 'target' in the data file
# df = pd.read_csv('./pred_input.csv')
tpot_data = pd.read_csv('./pred_input.csv',  dtype=np.float64)
tpot_data = tpot_data.rename(columns={'imdb_avgRating': 'target'})
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: -0.5314202493706478
exported_pipeline = make_pipeline(
    make_union(
        FunctionTransformer(copy),
        FunctionTransformer(copy)
    ),
    StackingEstimator(estimator=LassoLarsCV(normalize=True)),
    Normalizer(norm="max"),
    RandomForestRegressor(bootstrap=True, max_features=0.3, min_samples_leaf=11, min_samples_split=9, n_estimators=100)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)
print("start training ")
exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
print(r2_score(testing_target, results))