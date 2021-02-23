import tubesml as tml
import pytest

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline

import pandas as pd

import string
import random


def create_data():
    df, target = make_classification(n_features=10)
    
    i = 0
    random_names = []
    # generate n_features random strings of 5 characters
    while i < 10:
        random_names.append(''.join([random.choice(string.ascii_lowercase) for _ in range(5)]))
        i += 1
        
    df = pd.DataFrame(df, columns=random_names)
    df['target'] = target
    
    return df

df = create_data()


def test_gridsearch_bestestimator():
    '''
    Test grid_search returns an estimator ready to be used with no warnings
    '''
    y = df['target']
    df_1 = df.drop('target', axis=1)
    
    pipe_transf = Pipeline([('fs', tml.DtypeSel(dtype='numeric')), 
                     ('imp', tml.DfImputer(strategy='mean')), 
                     ('sca', tml.DfScaler(method='standard')), 
                     ('dummify', tml.Dummify()), 
                     ('pca', tml.PCADf(n_components=0.9))])
    pipe = tml.FeatureUnionDf([('transf', pipe_transf)])
    
    full_pipe = Pipeline([('pipe', pipe), 
                          ('logit', LogisticRegression(solver='lbfgs', multi_class='auto'))])
    
    param_grid = {'logit__C': [1, 2], 
                  'pipe__transf__sca__method': ['standard', 'robust', 'minmax'], 
                  'pipe__transf__imp__strategy': ['mean', 'median'], 
                  'pipe__transf__dummify__drop_first': [True, False], 
                  'pipe__transf__dummify__match_cols': [True, False], 
                  'pipe__transf__pca__n_components': [0.5, 3, 5]}
    
    result, best_param, best_estimator = tml.grid_search(data=df_1, target=y, estimator=full_pipe, 
                                                         param_grid=param_grid, scoring='accuracy', cv=3, random=False)
    
    with pytest.warns(None) as record:
        res = best_estimator.predict(df_1)
    assert len(record) == 0
    
    
def test_gridsearch_result():
    '''
    Test grid_search returns a dataframe summarizing the search results
    '''
    y = df['target']
    df_1 = df.drop('target', axis=1)
    
    pipe_transf = Pipeline([('fs', tml.DtypeSel(dtype='numeric')), 
                     ('imp', tml.DfImputer(strategy='mean')), 
                     ('sca', tml.DfScaler(method='standard')), 
                     ('dummify', tml.Dummify()), 
                     ('pca', tml.PCADf(n_components=0.9))])
    pipe = tml.FeatureUnionDf([('transf', pipe_transf)])
    
    full_pipe = Pipeline([('pipe', pipe), 
                          ('logit', LogisticRegression(solver='lbfgs', multi_class='auto'))])
    
    param_grid = {'logit__C': [1, 2], 
                  'pipe__transf__sca__method': ['standard', 'robust', 'minmax']}
    
    result, best_param, best_estimator = tml.grid_search(data=df_1, target=y, estimator=full_pipe, 
                                                         param_grid=param_grid, scoring='accuracy', cv=3, random=False)
    
    assert result.shape[0] == 6
    assert result.shape[1] == 10


def test_gridsearch_params():
    '''
    Test grid_search returns a dictionary of parameters with the best combination of parameters
    '''
    y = df['target']
    df_1 = df.drop('target', axis=1)
    
    pipe_transf = Pipeline([('fs', tml.DtypeSel(dtype='numeric')), 
                     ('imp', tml.DfImputer(strategy='mean')), 
                     ('sca', tml.DfScaler(method='standard')), 
                     ('dummify', tml.Dummify()), 
                     ('pca', tml.PCADf(n_components=0.9))])
    pipe = tml.FeatureUnionDf([('transf', pipe_transf)])
    
    full_pipe = Pipeline([('pipe', pipe), 
                          ('logit', LogisticRegression(solver='lbfgs', multi_class='auto'))])
    
    param_grid = {'logit__C': [1, 2], 
                  'pipe__transf__sca__method': ['standard', 'robust', 'minmax']}
    
    result, best_param, best_estimator = tml.grid_search(data=df_1, target=y, estimator=full_pipe, 
                                                         param_grid=param_grid, scoring='accuracy', cv=3, random=False)
    
    assert len(best_param.keys()) == len(param_grid.keys())
    

def test_randomsearch_bestestimator():
    '''
    Test grid_search returns an estimator ready to be used with no warnings when using random search
    '''
    y = df['target']
    df_1 = df.drop('target', axis=1)
    
    pipe_transf = Pipeline([('fs', tml.DtypeSel(dtype='numeric')), 
                     ('imp', tml.DfImputer(strategy='mean')), 
                     ('sca', tml.DfScaler(method='standard')), 
                     ('dummify', tml.Dummify()), 
                     ('pca', tml.PCADf(n_components=0.9))])
    pipe = tml.FeatureUnionDf([('transf', pipe_transf)])
    
    full_pipe = Pipeline([('pipe', pipe), 
                          ('logit', LogisticRegression(solver='lbfgs', multi_class='auto'))])
    
    param_grid = {'logit__C': [1, 2], 
                  'pipe__transf__sca__method': ['standard', 'robust', 'minmax'], 
                  'pipe__transf__imp__strategy': ['mean', 'median'], 
                  'pipe__transf__dummify__drop_first': [True, False], 
                  'pipe__transf__dummify__match_cols': [True, False], 
                  'pipe__transf__pca__n_components': [0.5, 3, 5]}
    
    result, best_param, best_estimator = tml.grid_search(data=df_1, target=y, estimator=full_pipe, 
                                                         param_grid=param_grid, scoring='accuracy', cv=3, random=20)
    
    with pytest.warns(None) as record:
        res = best_estimator.predict(df_1)
    assert len(record) == 0
    
    
def test_randomsearch_result():
    '''
    Test grid_search returns a dataframe summarizing the search results when using random search
    '''
    y = df['target']
    df_1 = df.drop('target', axis=1)
    
    pipe_transf = Pipeline([('fs', tml.DtypeSel(dtype='numeric')), 
                     ('imp', tml.DfImputer(strategy='mean')), 
                     ('sca', tml.DfScaler(method='standard')), 
                     ('dummify', tml.Dummify()), 
                     ('pca', tml.PCADf(n_components=0.9))])
    pipe = tml.FeatureUnionDf([('transf', pipe_transf)])
    
    full_pipe = Pipeline([('pipe', pipe), 
                          ('logit', LogisticRegression(solver='lbfgs', multi_class='auto'))])
    
    param_grid = {'logit__C': [1, 2], 
                  'pipe__transf__sca__method': ['standard', 'robust', 'minmax'], 
                  'pipe__transf__imp__strategy': ['mean', 'median'], 
                  'pipe__transf__dummify__drop_first': [True, False], 
                  'pipe__transf__dummify__match_cols': [True, False], 
                  'pipe__transf__pca__n_components': [0.5, 3, 5]}
    
    result, best_param, best_estimator = tml.grid_search(data=df_1, target=y, estimator=full_pipe, 
                                                         param_grid=param_grid, scoring='accuracy', cv=3, random=5)
    
    assert result.shape[0] == 5
    assert result.shape[1] == 14
    
    
def test_randomsearch_params():
    '''
    Test grid_search returns a dictionary of parameters with the best combination of parameters when using random search
    '''
    y = df['target']
    df_1 = df.drop('target', axis=1)
    
    pipe_transf = Pipeline([('fs', tml.DtypeSel(dtype='numeric')), 
                     ('imp', tml.DfImputer(strategy='mean')), 
                     ('sca', tml.DfScaler(method='standard')), 
                     ('dummify', tml.Dummify()), 
                     ('pca', tml.PCADf(n_components=0.9))])
    pipe = tml.FeatureUnionDf([('transf', pipe_transf)])
    
    full_pipe = Pipeline([('pipe', pipe), 
                          ('logit', LogisticRegression(solver='lbfgs', multi_class='auto'))])
    
    param_grid = {'logit__C': [1, 2], 
                  'pipe__transf__sca__method': ['standard', 'robust', 'minmax'], 
                  'pipe__transf__imp__strategy': ['mean', 'median'], 
                  'pipe__transf__dummify__drop_first': [True, False], 
                  'pipe__transf__dummify__match_cols': [True, False], 
                  'pipe__transf__pca__n_components': [0.5, 3, 5]}
    
    result, best_param, best_estimator = tml.grid_search(data=df_1, target=y, estimator=full_pipe, 
                                                         param_grid=param_grid, scoring='accuracy', cv=3, random=5)
    
    assert len(best_param.keys()) == len(param_grid.keys())
    