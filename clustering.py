import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings("ignore")
from sklearn.decomposition import PCA
from sklearn.preprocessing import MaxAbsScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.cluster import AgglomerativeClustering
import preprocess

def load_data(file, genes):
    
    cols = genes[0].split("\t")
    print(cols)

    # data = []
    # for x in file:
    #     print(x+"\n")
    print(file)
    # for i in range(0, len(file)):
    data = (file[0].split("\t"))

    y = []
    # # for i in range(0, len(data)):
    # y.append(data[0][0])
    y.append(data.pop(0))
    content = []
    for i in range(0, len(data)):
        content.append(data[i])
    print(content)
    # print(y)

    df = pd.DataFrame(content,index=y, columns = cols)
    return df



def run_clustering_KMeans(pca_data_maxAbs):
    inertias = []

    for i in range(1,11):
        kmeans = KMeans(n_clusters=i,init="random",random_state=32)
        kmeans.fit(pca_data_maxAbs)
        inertias.append(kmeans.inertia_) #append to the array, sum of squared distances of samples to their nearest cluster center

    # plt.plot(range(1,11), inertias, marker='o')
    # plt.grid()
    # plt.title('Elbow method')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('Inertia')
    # plt.show()

    kmeans = KMeans(init = "random", n_clusters=2, random_state=42)
    clusters = kmeans.fit_predict(pca_data_maxAbs)
    return clusters

def results(clusters, pca_data_maxAbs):
    # plt.scatter(pca_data_maxAbs[:, 0], pca_data_maxAbs[:, 1], c=clusters, cmap='viridis')
    # plt.xlabel('Principal Component 1')
    # plt.ylabel('Principal Component 2')
    # plt.title('PCA followed by KMeans Clustering')
    # plt.colorbar(label='Cluster')
    # plt.show()
    score = silhouette_score(pca_data_maxAbs, clusters)
    return score

def run_clustering_agc(pca_data):
    def agg_clustering(metric, data, cluster_number):
        agc = AgglomerativeClustering(n_clusters=cluster_number,metric=metric, linkage="average", distance_threshold=None)
        clusters=agc.fit_predict(data)
        score = silhouette_score(data,agc.labels_,metric=metric)
        return clusters, score
    clusters_eu, score_eu = agg_clustering("euclidean", pca_data, 2)
    clusters_manhattan, score_manhattan = agg_clustering("manhattan", pca_data, 2)
    clusters_cosine, score_cosine = agg_clustering("cosine", pca_data, 2)
    return clusters_eu, clusters_manhattan, clusters_cosine, score_eu, score_manhattan, score_cosine

def main(data, genes):  
    df = load_data(data,genes)
    pca_data_maxAbs, pca_data_stdScaler = preprocess.preprocess_data(df)
    def clustering_data(data):
        clusters = run_clustering_KMeans(data)
        silhouette_score = results(clusters,data)
        clusters_eu, clusters_manhattan, clusters_cosine, score_eu, score_manhattan, score_cosine = run_clustering_agc(data)
        metric = max(score_cosine, score_eu, score_manhattan)
        if metric == score_cosine:
            clusters_agc = clusters_cosine
        elif metric == score_eu:
            clusters_agc = clusters_eu
        else:
            clusters_agc = clusters_manhattan
        return clusters, silhouette_score,clusters_agc, 

    clusters_kmeans_maxAbs, s_score_kmeans_maxAbs, clusters_agc_maxAbs, s_score_agc_maxAbs = clustering_data(pca_data_maxAbs)
    clusters_kmeans_stdScaler,s_score_kmeans_stdScaler, clusters_agc_stdScaler, s_score_agc_stdScaler = clustering_data(pca_data_stdScaler)
    preprocessor_kmeans = max(s_score_kmeans_maxAbs,s_score_kmeans_stdScaler)
    preprocessor_agc = max(s_score_agc_maxAbs, s_score_agc_stdScaler)
    if preprocessor_kmeans == s_score_kmeans_maxAbs and preprocessor_agc == s_score_agc_maxAbs:
        return clusters_kmeans_maxAbs, s_score_kmeans_maxAbs, clusters_agc_maxAbs, s_score_agc_maxAbs
    elif preprocessor_kmeans == s_score_kmeans_stdScaler and preprocessor_agc == s_score_agc_stdScaler:
        return clusters_kmeans_stdScaler, s_score_kmeans_stdScaler, clusters_agc_stdScaler, s_score_agc_stdScaler


    # df.to_csv("data.csv")
    # return clusters, pca_data_maxAbs[:,0], pca_data_maxAbs[:,1]