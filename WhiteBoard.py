# Colin's Whiteboard
# ML_Brainstem 2024

# Loading global packages
from typing import List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from mpl_toolkits.mplot3d import Axes3D  # Import for 3-D plotting
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Choosing a matplotlib backend to ensure plot pop-up will deploy
import matplotlib

matplotlib.use('TkAgg')


def generate_clustering_results(file_path: str, n_clusters: int) -> List[int]:
    df = pd.read_csv(file_path, header=0, float_precision='high')
    kmeans: KMeans = KMeans(n_clusters=n_clusters, random_state=25)
    cluster_labels: List[int] = kmeans.fit_predict(df)

    # Visualizing the clustering results using PCA (with 3 components)
    pca = PCA(n_components=3)
    reduced_data = pca.fit_transform(df)
    reduced_df = pd.DataFrame(reduced_data, columns=['PC1', 'PC2', 'PC3'])
    reduced_df['Cluster'] = cluster_labels

    # Generating 3-D scatter plot
    # For now, hold off on the visualizations

    return cluster_labels


def brain_kmeansREDUX():
    """
    Loads a CSV file based on a provided filepath and performs K-Means clustering based on the data frame contained

    :return: Cluster labels
    """

    # User greeting
    print("\nHey Colin! This is brain_kmeansREDUX(). Booting up protocol now...")

    # Asking for filepath to be analyzed
    filepath = input("\nEnter file to be k-mean'ed: ")

    # Loading CSV file with pandas package
    df = pd.read_csv(filepath, header=0, float_precision='high')

    # Printing head table to ensure proper loading of data
    print(f"\nHEAD TABLE OF LOADED DATA FRAME: {filepath}")
    print(df.head())

    # Asking for a max number of clusters
    max_clusters = int(input("\nEnter the maximum number of k-means clusters: "))

    # Calculating the SSEs within clusters (the inertias)
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=35)
        kmeans.fit(df)
        inertias.append(kmeans.inertia_)

    # Plotting knee plot
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, max_clusters + 1), inertias, marker='o')
    plt.title('\nKnee Plot for K-Means')
    plt.xlabel('Number of k-clusters')
    plt.ylabel('Intertia (SSE within clusters)')
    plt.grid(True)

    # Calculating silhouette scores for given number of clusters
    silhouette_scores = []
    for k in range(2, max_clusters + 2):
        kmeans = KMeans(n_clusters=k, random_state=35)
        labels = kmeans.fit_predict(df)
        silhouette_avg = silhouette_score(df, labels)
        silhouette_scores.append(silhouette_avg)

    # Plotting silhouette plot
    plt.subplot(1, 2, 2)
    plt.plot(range(1, max_clusters + 1), silhouette_scores, marker='o')
    plt.title("\nSilhouette Plot for K-Means")
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Asking user for the number of clusters they would like to set for clustering protocol
    cluster_set = int(input("\nBased on the previous results, how many clusters would you like to set?: "))

    # Performing k-means
    kmeans = KMeans(n_clusters=cluster_set, random_state=25)
    cluster_labels = kmeans.fit_predict(df)

    # Visualizing the clustering results using PCA (with 3 components)
    pca = PCA(n_components=3)
    reduced_data = pca.fit_transform(df)
    reduced_df = pd.DataFrame(reduced_data, columns=['PC1', 'PC2', 'PC3'])
    reduced_df['Cluster'] = cluster_labels

    # Generating 3-D scatter plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(reduced_df['PC1'], reduced_df['PC2'], reduced_df['PC3'], c=cluster_labels, cmap='viridis')
    ax.set_title('K-Means Clustering Results (3-D Projection)')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')

    plt.show()

    # Returning the cluster labels
    return(cluster_labels)

###################################################################################################################
def brain_kmeansREDUX2():
    """
    Loads a CSV file based on a provided filepath and performs K-Means clustering based on the data frame contained

    :return: Cluster labels
    """

    # User greeting
    print("\nHey Colin! This is brainREDUX2(). Booting up protocol now...")

    # Asking for filepath to be analyzed
    filepath = input("\nEnter file to be k-mean'ed: ")

    # Loading CSV file with pandas package
    df = pd.read_csv(filepath, header=0, float_precision='high')

    # Printing head table to ensure proper loading of data
    print(f"\nHEAD TABLE OF LOADED DATA FRAME: {filepath}")
    print(df.head())

    # Asking for a max number of clusters
    max_clusters = int(input("\nEnter the maximum number of k-means clusters: "))

    # Calculating the SSEs within clusters (the inertias)
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=35)
        kmeans.fit(df)
        inertias.append(kmeans.inertia_)

    # Plotting knee plot
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, max_clusters + 1), inertias, marker='o')
    plt.title('\nKnee Plot for K-Means')
    plt.xlabel('Number of k-clusters')
    plt.ylabel('Intertia (SSE within clusters)')
    plt.grid(True)

    # Calculating silhouette scores for given number of clusters
    silhouette_scores = []
    for k in range(2, max_clusters + 2):
        kmeans = KMeans(n_clusters=k, random_state=35)
        labels = kmeans.fit_predict(df)
        silhouette_avg = silhouette_score(df, labels)
        silhouette_scores.append(silhouette_avg)

    # Plotting silhouette plot
    plt.subplot(1, 2, 2)
    plt.plot(range(1, max_clusters + 1), silhouette_scores, marker='o')
    plt.title("\nSilhouette Plot for K-Means")
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Asking user for the number of clusters they would like to set for clustering protocol
    cluster_set = int(input("\nBased on the previous results, how many clusters would you like to set?: "))

    # Asking user for the three features to use for 3-D projection
    x_feature = input("\nEnter the name of the feature for the x-axis: ")
    y_feature = input("Enter the name of the feature for the y-axis: ")
    z_feature = input("Enter the name of the feature for the z-axis: ")

    # Performing k-means
    kmeans = KMeans(n_clusters=cluster_set, random_state=25)
    cluster_labels = kmeans.fit_predict(df)

    # Generating 3-D scatter plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df[x_feature], df[y_feature], df[z_feature], c=cluster_labels, cmap='viridis')
    ax.set_title('K-Means Clustering Results (3-D Projection)')
    ax.set_xlabel(x_feature)
    ax.set_ylabel(y_feature)
    ax.set_zlabel(z_feature)

    plt.show()

    # Returning the cluster labels
    return(cluster_labels)


if __name__ == '__main__':
    brain_kmeansREDUX()
