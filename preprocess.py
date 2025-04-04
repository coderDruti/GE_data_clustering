import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from sklearn.decomposition import PCA
from sklearn.preprocessing import MaxAbsScaler, StandardScaler

def standardize_data_maxAbs(df):
    scaler = MaxAbsScaler()
    X_train_maxAbs = scaler.fit_transform(df)
    return X_train_maxAbs

def standardize_data_stdScaler(df):
    X_train_stdScaler = StandardScaler().fit_transform(df)
    return X_train_stdScaler

def pca(X_train):
    pca = PCA(n_components=1)
    pca_data = pca.fit_transform(X_train)
    return pca_data

def preprocess_data(df):
    return pca(standardize_data_maxAbs(df)), pca(standardize_data_stdScaler(df))