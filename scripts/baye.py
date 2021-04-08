from numpy import mean
from sklearn.model_selection import cross_val_score
from skopt.utils import use_named_args
from skopt import gp_minimize
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from skopt.space import Integer,Real,Categorical

df = pd.read_csv('./pred_input.csv')
print(df.shape)
X,y = df.drop(['imdb_avgRating'],axis=1), df['imdb_avgRating']
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

model = RandomForestRegressor()
search_space = [Integer(100, 1000, name='n_estimators'), \
                Integer(10, 150, name='max_depth'), \
                Integer(2, 20, name='min_samples_split'), \
                Real(0.0, 1.0, name='max_features'), \
                Integer(1, 8, name='min_samples_leaf')]
# define the function used to evaluate a given configuration
@use_named_args(search_space)
def evaluate_model(**params):
	# something
	model.set_params(**params)
	# calculate 5-fold cross validation
	result = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
	# calculate the mean of the scores
	estimate = mean(result)
	return 1.0 - estimate
 
# perform optimization
result = gp_minimize(evaluate_model, search_space)
# summarizing finding:
print('Best Accuracy: %.3f' % (1.0 - result.fun))
print('Best Parameters: ' % (result.x))