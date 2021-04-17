## This folder contains all the helper scripts

#### tmdb_api.py
```
cd ..
python script/tmdb_api.py
```
This script will call the TMDB API to grab the movie data.
#### tpot_auto.py
```
cd ..
python script/tpot_auto.py
```
This script will use TPOT AutoML framework to train the movie rating predictor.

#### query_database.py
This query is the MongoDB API we made. You should be able to query data with different movie release years range, store/get trained models, etc. 

#### pred_util.py
This script was used as a helper function in data processing for rating predictor.

#### pred_param_tuning.py
```
cd ..
python script/pred_param_tuning.py
```
This script will use Random Search method to tune the Hyperparameters for rating predictor model.

#### pred_model.py
```
cd ..
python script/pred_model.py
```
This script will train 4 different regression model and plot & print and accuracy results. 

#### pred_feature_selection.py
```
cd ..
python script/pred_feature_selection.py
```
This script will first remove high-correlated features and run RFECV with random forest regressor.  
#### auto_ml.py
This script used auto-sklearn AutoML framework. 
