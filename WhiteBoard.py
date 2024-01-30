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

# Local packages
from lib.string_parse import string_to_int_list

# Choosing a matplotlib backend to ensure plot pop-up will deploy
import matplotlib

matplotlib.use('TkAgg')


def generate_clustering_results(file_path: str, n_clusters: int) -> List[int]:
    """
    Loads a CSV file based on a provided filepath and performs K-Means clustering based on the data frame contained
    (This is a snippet of Colin's Code that I just put into a separate function, so this is Colin's code)
    
    :param file_path: The path to the file
    :param n_clusters: The number of clusters to generate
    :return: Cluster labels
    """
    df = pd.read_csv(file_path, header=0, float_precision='high')
    kmeans: KMeans = KMeans(n_clusters=n_clusters, random_state=25)
    cluster_labels: List[int] = kmeans.fit_predict(df)

    return cluster_labels


###################################################################################################################


def brain_kmeans_cbk():
    """
    Loads a CSV file based on a provided filepath and performs K-Means clustering based on the data frame contained
    :return: Cluster labels
    """

    name = input("What is your name? ")
    print(f"\nHey {name}! This is brain_kmeans_cbk(). Doing some cool stuff now...")

    # Asking for filepath to be analyzed
    filepath = input("\nEnter file to be k-mean'ed: ")

    # Loading CSV file with pandas package
    df = pd.read_csv(filepath, header=0, float_precision='high')
    new_df = {}

    # Printing head table to ensure proper loading of data
    print(f"\nHEAD TABLE OF LOADED DATA FRAME: {filepath}")
    print(df.head())

    # Asking for a max number of clusters
    max_clusters = int(input("\nEnter the maximum number of k-means clusters: "))

    # Calculating the SSEs within clusters (the inertia's)

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
    plt.ylabel('Inertia (SSE within clusters)')
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
    cluster_set = string_to_int_list(
        input("\nBased on the previous results, how many clusters would you like to set?: "))

    # Performing k-means

    cluster_results = []

    for i in range(len(cluster_set)):
        kmeans = KMeans(n_clusters=cluster_set[i], random_state=25)
        cluster_labels = kmeans.fit_predict(df)

        new_df[f'cluster_{cluster_set[i]}'] = cluster_labels

        # Appending the cluster results to the cluster_results list
        cluster_results.append(cluster_labels)

        # Visualizations would go here

    # Load the XYZ data from the mutated dataset
    xyz_dfs = pd.read_csv('data_files/output_K1_mutate.csv', header=0, float_precision='high')

    # Add all the gene data to the df_data

    for (columnName, columnData) in xyz_dfs.items():
        new_df[columnName] = columnData

    df = pd.DataFrame(new_df)

    print(df.head())

    wants_to_save = input("Would you like to save the data frame to a CSV file? (y/n): ")

    if wants_to_save.lower() in ['y', 'yes', 'yeah', 'yep', 'yup']:
        name_of_file = input("What would you like to name the file?: ")
        name_of_file = name_of_file.replace(".csv", "")

        df.to_csv(f"{name_of_file}.csv", index=False)

        print(f"File saved as {name_of_file}.csv")

    # Returning the list of cluster results
    return cluster_results


if __name__ == '__main__':
    brain_kmeans_cbk()
