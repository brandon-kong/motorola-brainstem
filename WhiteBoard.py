# Colin's Whiteboard
# ML_Brainstem 2024

# Loading global packages
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

# Local packages
from lib.string_parse import string_to_int_list

# Choosing a matplotlib backend to ensure plot pop-up will deploy
import matplotlib
from matplotlib import cm

matplotlib.use('TkAgg')


cluster_label_prefix = 'cluster_'

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


def brain_kmeans_cbk() -> List[List[int]]:
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

    # Plotting the knee plot
    plot_knee_plot(max_clusters, inertias)

    # Calculating silhouette scores for given number of clusters
    silhouette_scores = []
    for k in range(2, max_clusters + 2):
        kmeans = KMeans(n_clusters=k, random_state=35)
        labels = kmeans.fit_predict(df)
        silhouette_avg = silhouette_score(df, labels)
        silhouette_scores.append(silhouette_avg)

    # Plotting silhouette plot
    plot_silhouette_plot(max_clusters, silhouette_scores)

    # Displaying the plots

    plt.tight_layout()
    plt.show(block=False)

    # Asking user for the number of clusters they would like to set for clustering protocol
    cluster_set = string_to_int_list(
        input("\nBased on the previous results, how many clusters would you like to set?: "))

    # Performing k-means

    cluster_results: List[List[int]] = []

    for i in range(len(cluster_set)):
        cluster_labels = do_kmeans_clustering(df, cluster_set[i])

        new_df[f'{cluster_label_prefix}{cluster_set[i]}'] = cluster_labels

        # Appending the cluster results to the cluster_results list
        cluster_results.append(cluster_labels)

        # Visualizations would go here
        visualize_clusters(filepath)

    # Load the XYZ data from the mutated dataset
    xyz_dfs = pd.read_csv('data_files/output_K1_mutate.csv', header=0, float_precision='high')

    # Add all the gene data to the df_data

    for (columnName, columnData) in xyz_dfs.items():
        if (columnName in df) or columnName in ['X', 'Y', 'Z']:
            new_df[columnName] = columnData

    df = pd.DataFrame(new_df)

    print(df.head())

    wants_to_save = input("Would you like to save the data frame to a CSV file? (y/n): ")

    if wants_to_save.lower() in ['y', 'yes', 'yeah', 'yep', 'yup']:
        name_of_file = input("What would you like to name the file?: ").replace(".csv", "")

        df.to_csv(f"{name_of_file}.csv", index=False)

        print(f"File saved as {name_of_file}.csv")

    print(f"Have a nice day, {name}!")

    # Returning the list of cluster results
    return cluster_results


def plot_knee_plot(max_clusters: int, inertias: List[float]):
    """
    Plots the knee plot for the k-means clustering

    :param max_clusters:
    :param inertias:
    :return:
    """

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, max_clusters + 1), inertias, marker='o')
    plt.title('\nKnee Plot for K-Means')
    plt.xlabel('Number of k-clusters')
    plt.ylabel('Inertia (SSE within clusters)')
    plt.grid(True)


def plot_silhouette_plot(max_clusters: int, scores: List[float]):
    """
    Plots the silhouette plot for the k-means clustering

    :param max_clusters:
    :param scores:
    :return:
    """

    plt.subplot(1, 2, 2)
    plt.plot(range(1, max_clusters + 1), scores, marker='o')
    plt.title("\nSilhouette Plot for K-Means")
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.grid(True)


def do_kmeans_clustering(data: pd.DataFrame, n_clusters: int) -> List[int]:
    """
    Performs K-Means clustering on a given data frame

    :param data: The data frame to perform K-Means clustering on
    :param n_clusters: The number of clusters to generate
    :return: Cluster labels
    """
    kmeans: KMeans = KMeans(n_clusters=n_clusters, random_state=25)
    cluster_labels: List[int] = kmeans.fit_predict(data)

    return cluster_labels



def visualize_clusters(df_to_visualize: str):

    df = pd.read_csv(df_to_visualize, header=0, float_precision='high')

    

    x = df['X']
    y = df['Y']
    z = df['Z']
    
    # Scatter plot with colored points based on cluster_id

    cluster_labels = get_cluster_labels_from_df(df)

    for i in range(len(cluster_labels)):

        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        label = cluster_labels[i].get('label')
        data = cluster_labels[i].get('data')

        ax.set_title(f'Cluster label for {label}')

        cmap = cm.get_cmap('rainbow', max(data) + 1)

        scatter = ax.scatter(x, y, z, c=data, cmap=cmap, alpha=0.6)
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        # Add a colorbar
        colorbar = fig.colorbar(scatter, ax=ax, label='Cluster ID')

    # Show the plot
        plt.show(block=True)

    # Customize the plot
    
    

def get_cluster_labels_from_df(df: pd.DataFrame) -> List[List[int]]:

    labels = []

    for (columnName, columnData) in df.items():
        strColName = str(columnName)

        if strColName.startswith(cluster_label_prefix):
            labels.append({
                'label': columnName,
                'data': columnData
            })

    return labels


if __name__ == '__main__':
    visualize_clusters('data_files/generated/gas6_clustered_xyz.csv')
