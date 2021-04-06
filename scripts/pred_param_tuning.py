from scipy.stats import loguniform
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
import numpy as np
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

def random_search_param(param_dict, model, cv, X, y, name):
    print(f'***********STARTING***********')
    search = RandomizedSearchCV(model, param_dict, n_iter=10, scoring='neg_mean_absolute_error', cv=cv, random_state=1)
    result = search.fit(X, y)
    print(f'***********{name}***********')
    print('Best Score: %s' % result.best_score_)
    print('Best Hyperparameters: %s' % result.best_params_)


if __name__ == '__main__':
    # load dataset
    df = pd.read_csv('./pred_input.csv')
    print(df.shape)
    X,y = df.drop(['imdb_avgRating'],axis=1), df['imdb_avgRating']
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)

    cv = RepeatedKFold(n_splits=5, n_repeats=8, random_state=8)
    rf = RandomForestRegressor()
    rf_space = dict()
    rf_space['n_estimators'] = np.arange(100, 1000, 25).tolist()
    rf_space['max_depth'] = [int(x) for x in np.linspace(start = 10, stop = 150, num = 10)]
    rf_space['min_samples_split'] = np.arange(2, 20, 3).tolist()
    rf_space['max_features'] = np.arange(0, 1, 0.15).tolist()
    rf_space['bootstrap'] = [True, False]
    rf_space['min_samples_leaf'] = [1, 2, 4, 6]
    random_search_param(rf_space, rf, cv, X_train, y_train, "RandomForestRegressor")

    xgb = XGBRegressor()
    xgb_space = dict()
    xgb_space['learning_rate'] = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    xgb_space['max_depth'] = [ 3, 4, 5, 6, 8, 10, 12, 15]
    xgb_space['min_child_weight'] = [ 1, 3, 5, 7 ]
    xgb_space['gamma'] = [ 0.0, 0.1, 0.2 , 0.3, 0.4 ]
    xgb_space['colsample_bytree'] = [ 0.3, 0.4, 0.5 , 0.7 ]
    random_search_param(xgb_space, xgb, cv, X_train, y_train, "XGBRegressor")
