#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Created on Thu Aug 16 18:23:28 2018

@author: oluwaseyiawoga
"""

"""
Created on Sun Jul 29 13:00:54 2018

@author: oluwaseyiawoga

Reference: Python Machine Learning Packt Books 2nd Edition
           Sebastian Raschka & Vahid Mirjalili

           Introduction to Data Science - WQU/Data Incubator

           Sklearn Online Documentation

           WQU Machine Learning Course Materials & Learning Videos
           
DATA:
creditcards.csv - https://www.kaggle.com/mlg-ulb/creditcardfraud

DATA INSTRUCTIONS - Download the above data from Kaggle and save in the 
same folder as the python file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (12.0, 8.0)
np.warnings.filterwarnings('ignore')
from pylab import rcParams
rcParams['figure.figsize'] = 10, 8
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LassoCV
from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import seaborn as sns
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as mse
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import roc_auc_score


if __name__ == '__main__':
    """
    Import the Wine Data Using Pandas
    """

    df = pd.read_csv("creditcard.csv")

    """
    Split the Data into Train/Test Split
    """

    X, y = df.iloc[:, 0:-1].values, df.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0, stratify=y)

    """
    Select the feature and target labels
    """
    feature_labels = df.columns[0:-1].values

    target_label = df.columns[-1:].values

    """
    Feature Selection Using Random Forest
    """

    forest = RandomForestClassifier(n_estimators=500, random_state=1)

    forest.fit(X_train, y_train)
    importances = forest.feature_importances_

    indices = np.argsort(importances)[::-1]

    print("")
    print("Feature Importance Ranking Using RandomForest")
    print("")
    for f in range(X_train.shape[1]):
        print("%2d) %-*s%f" %
              (f + 1, 30, feature_labels[indices[f]], importances[indices[f]]))

    plt.title("Feature Importance")
    plt.bar(range(X_train.shape[1]), importances[indices], align='center')

    plt.xticks(range(X_train.shape[1]), feature_labels, rotation=90)
    plt.xlim([-1, X_train.shape[1]])
    plt.tight_layout()
    plt.show()

    """
    Test on Important Labels Only
    """

    df2 = df[["V17", "V14", "V12", "V10", "V16", "V11", "V7", "Class"]]

    X, y = df2.iloc[:, 0:-1].values, df2.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=30, stratify=y)

    feature_labels = df2.columns[0:-1].values

    target_label = df2.columns[-1:].values

    pipe_lr = make_pipeline(
        StandardScaler(), PCA(
            n_components=2), LogisticRegression(
                random_state=1))

    pipe_lr.fit(X_train, y_train)
    y_pred = pipe_lr.predict(X_test)
    print("")
    print("Logistic Regression Test Accuracy Using a Subset of the \n Feature Labels Based on Output from Random Forest: ")
    print("")
    print('Test Accuracy: %.3f' % pipe_lr.score(X_test, y_test))

    print("")
    print("Confusion Matrix of the Ensemble Model: ")
    print("")
    data = metrics.confusion_matrix(y_test, y_pred)
    confusionMatrix = pd.DataFrame({'Pred: 0': data[:,
                                                    0],
                                    'Pred: 1': data[:,
                                                    1]})
    confusionMatrix["Actual"] = [0, 1]
    confusionMatrix.set_index(confusionMatrix["Actual"], inplace=True)
    del confusionMatrix["Actual"]
    print(confusionMatrix)
    print("")

    """
    Using Ensemble Model
    """

    features = df.columns[0:-1].values

    class FeatureSelectTransformer(BaseEstimator, TransformerMixin):
        def __init__(self, columns):
            self.columns = columns
            self.indices = [i for i, feature in enumerate(
                features) if feature in self.columns]
            if len(self.indices) < 1:
                raise ValueError('Need to Select at one Feature')

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            return [[ele for i, ele in enumerate(
                row) if i in self.indices] for row in X]

    feature_labels_1 = ["V17", "V14", "V12", "V10", "V16", "V11", "V7"]
    feature_labels_2 = [
        "V17",
        "V14",
        "V12",
        "V10",
        "V16",
        "V11",
        "V7",
        "Amount"]
    feature_labels_3 = ["V17", "V14", "V12", "V10", "V16"]

    ft = FeatureSelectTransformer(feature_labels_1)
    ft2 = FeatureSelectTransformer(feature_labels_2)
    ft3 = FeatureSelectTransformer(feature_labels_3)

    class PredictTransform(BaseEstimator, TransformerMixin):
        def __init__(self, model):
            self.model = model

        def fit(self, X, y=None):
            self.model.fit(X, y)
            return self

        def transform(self, X):
            return [[i] for i in self.model.predict(X)]

    union = FeatureUnion([
        ('a_model', Pipeline([
            ('select', ft2),
            ('Logistic', PredictTransform(RandomForestClassifier(n_estimators=50)))
        ])),
        ('b_model', Pipeline([
            ('select', ft2),
            ('Logistic', PredictTransform(LogisticRegression()))
        ])),

        ('c_model', Pipeline([
            ('select', ft3),
            ('Logistic', PredictTransform(KNeighborsClassifier(n_neighbors=50)))
        ]))

    ])

    model = Pipeline([
        ('scaler', StandardScaler()),
        ('scaler2', MinMaxScaler()),
        ('union', union),
        ('Blender', KNeighborsClassifier(n_neighbors=50))
    ])

    X, y = df.iloc[:, 0:-1].values, df.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=30, stratify=y)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("")
    print("Ensemble Model Test Accuracy Using a Subset of the \n Feature Labels Based on Output from Random Forest: ")
    print("")
    print('Test Accuracy: %.3f' % model.score(X_test, y_test))

    blended = model.predict(X_test)

    print("")
    print("Confusion Matrix of the Ensemble Model: ")
    print("")
    data = metrics.confusion_matrix(y_test, y_pred)
    confusionMatrix = pd.DataFrame({'Pred: 0': data[:,
                                                    0],
                                    'Pred: 1': data[:,
                                                    1]})
    confusionMatrix["Actual"] = [0, 1]
    confusionMatrix.set_index(confusionMatrix["Actual"], inplace=True)
    del confusionMatrix["Actual"]
    print(confusionMatrix)
    print("")

    print("Accuracy", metrics.accuracy_score(y_test, y_pred))
    print("")
    print("AUC", metrics.roc_auc_score(y_test, y_pred))
    print("")

    y_pred_proba = model.predict_proba(X_test)[::, 1]
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = roc_auc_score(y_test, y_pred_proba)
    plt.plot(fpr, tpr, label="Train/Test Split, AUC=" + str(auc))
    plt.legend(loc=4)
    plt.show()
