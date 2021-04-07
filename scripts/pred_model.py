from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import VotingRegressor
import math
import pickle
SAVE_MODEL = True

def plot_pred_valid(name, y_valid, y_pred):
    fig, ax = plt.subplots()
    ax.scatter(y_valid, y_pred)
    ax.plot([0, 10], [0, 10], 'k--', lw=3)
    ax.set_xlabel('Ground Truth rating')
    ax.set_ylabel('Predicted rating')
    plt.title('Measured versus predicted rating')
    plt.ylim((2, 9)) 
    plt.xlim(2, 9)   
    # plt.show()
    plt.savefig(f'pred_results_imgs/{name}.png')

def define_models():
    # linear regression
    reg_model = LinearRegression()
    xgb_model = XGBRegressor(colsample_bytree= 0.6, gamma= 0.7, max_depth= 4, objective='reg:squarederror')
    ada = AdaBoostRegressor(random_state=0, n_estimators=100)
    # rf = make_pipeline(
    #     MinMaxScaler(),
    #     RandomForestRegressor(bootstrap=True, max_features=0.15000000000000002, min_samples_leaf=6, min_samples_split=16, n_estimators=100)
    # )
    rf = RandomForestRegressor(bootstrap=True, max_features=0.15000000000000002, min_samples_leaf=6, min_samples_split=16, n_estimators=100)
    # svr = SVR(C=1.0, epsilon=0.2)
    er = VotingRegressor([('rf', rf),('xgb_model', xgb_model)])

    return [reg_model, xgb_model, ada, rf,  er]

def print_statistics(y_valid, y_pred):
    print(f'The R^2 score is {r2_score(y_valid, y_pred)}')
    print(f'The MSE score is {mean_squared_error(y_valid, y_pred)}')
    print(f'The MAE score is {mean_absolute_error(y_valid, y_pred)}')
    print(f'The RMSE score is {math.sqrt(mean_squared_error(y_valid, y_pred))}\n')

def plotFeaturesRanking(rf, cols):
    print("Plotting features ranking...")
    features = cols
    importances = rf.feature_importances_
    indices = np.argsort(importances)
    plt.figure(figsize=(25,8))
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    # plt.show()
    plt.savefig('pred_results_imgs/feature_importance.png')


if __name__ == '__main__':
    df = pd.read_csv('./pred_input.csv')
    print(df.shape)
    df.dropna(inplace=True)
    X,y = df.drop(['imdb_avgRating'],axis=1), df['imdb_avgRating']
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    models_names = ['LinearRegression', \
                    'XGBRegressor', \
                    'AdaBoostRegressor', \
                    'RandomForestRegressor', \
                    'VotingRegressor']
    models = define_models()
    for i, m in enumerate(models):
        print(f'{models_names[i]} training results: ')
        m.fit(X_train, y_train)
        y_pred = m.predict(X_valid)
        print_statistics(y_valid, y_pred)
        plot_pred_valid(models_names[i], y_valid, y_pred)
    
    plotFeaturesRanking(models[3],X_train.columns.tolist())
    if SAVE_MODEL:
        filename = 'random_forest_model.pkl'
        pickle.dump(models[3], open(filename, 'wb'))