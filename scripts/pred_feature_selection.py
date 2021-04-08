import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.svm import SVC, SVR
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# Calculate the correlation coefficient between features and keep the one between highly correctled features
def corr_features(X):
    correlated_features = set()
    correlation_matrix = X.corr()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > 0.8:
                colname = correlation_matrix.columns[i]
                correlated_features.add(colname)
    print(f'{correlated_features} is highly corrected with other features, thus remove for now')
    newX = X.drop(correlated_features,axis=1)
    return newX

# It will plot the optimal number of feature based on the randon forest model
def optimal_num_features(X,y):
    print("Ploting optimal number of features...")
    rf = RandomForestRegressor(max_depth=10,min_samples_split=10, min_samples_leaf=10,random_state=101)
    rfecv = RFECV(estimator=rf, step=1, cv=4, scoring='r2')
    rfecv.fit(X, y)
    # rfecv.show()
    plt.figure(figsize=(16, 9))
    plt.title('Recursive Feature Elimination with Cross-Validation (REFCV)', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Number of features selected', fontsize=14, labelpad=20)
    plt.ylabel('Score', fontsize=14, labelpad=20)
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_, color='#303F9F', linewidth=3)
    # plt.show()
    plt.savefig('02.png')
    # print(rfecv.estimator_.feature_importances_)
    return rfecv

# It will polt the features importance graph 
def plotFeaturesRanking(rfecv,X):
    print("Plotting features ranking...")
    features = X.columns
    importances = rfecv.estimator_.feature_importances_
    indices = np.argsort(importances)
    plt.figure(figsize=(25,8))
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    # plt.show()
    plt.savefig('01.png')

if __name__ == '__main__':
    df = pd.read_csv('./pred_input.csv')
    X,y = df.drop(['imdb_avgRating'],axis=1), df['imdb_avgRating']
    # print(X.corr())
    newX = corr_features(X)
    assert X.shape[0] == newX.shape[0]
    rfecv = optimal_num_features(newX,y)
    plotFeaturesRanking(rfecv,newX)