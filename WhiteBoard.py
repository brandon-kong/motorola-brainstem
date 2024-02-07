# Colin's Whiteboard
# ML_Brainstem 2024

# Loading global packages
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

from lib.visualizer import show_stacked_bar_graph

# Local packages

# Choosing a matplotlib backend to ensure plot pop-up will deploy
import matplotlib
from matplotlib import cm, colormaps

matplotlib.use('TkAgg')

cluster_label_prefix = 'cluster_'


def string_to_int_list(string_as_list: str) -> List[int]:
    """
    Converts a string of format "[a1,b1,c1,d1,e1]" to a list of lists
    :param string_as_list: A string of format "[1,2,3]"
    :return: A list of integers
    """

    # Remove brackets at the end of they exist

    string_as_list = string_as_list.replace("[", "").replace("]", "").replace(" ", "")

    split_string = string_as_list.split(",")

    return list(map(int, split_string))



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


def brain_kmeans_cbk() -> pd.DataFrame:
    """
    Loads a CSV file based on a provided filepath and performs K-Means clustering based on the data frame contained
    :return: The dataframe generated with the cluster ids, XYZ, and the genes
    """

    # User greeting
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
        occurrences = {}

        for label in cluster_labels:
            if label in occurrences:
                occurrences[label] += 1
            else:
                occurrences[label] = 1

        print(f"\nCluster Occurrences for {cluster_set[i]} clusters: {occurrences}")

    # Load the XYZ data from the mutated dataset
    xyz_dfs = pd.read_csv('data_files/output_K1_mutate.csv', header=0, float_precision='high')

    # Add all the gene data to the df_data

    for (columnName, columnData) in xyz_dfs.items():
        if (columnName in df) or columnName in ['X', 'Y', 'Z']:
            new_df[columnName] = columnData

    # Add the focused genes to the df_data as well

    for (columnName, columnData) in df.items():
        if columnName in df:
            new_df[columnName] = columnData

    df = pd.DataFrame(new_df)

    print(df.head())

    # Visualize the clusters
    visualize_clusters(df)

    wants_to_save = input("Would you like to save the data frame to a CSV file? (y/n): ")

    if wants_to_save.lower() in ['y', 'yes', 'yeah', 'yep', 'yup']:
        name_of_file = input("What would you like to name the file?: ").replace(".csv", "")

        df.to_csv(f"{name_of_file}.csv", index=False)

        print(f"File saved as {name_of_file}.csv")

    print(f"Have a nice day, {name}!")

    # Returning the list of cluster results
    return df


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


def visualize_clusters(df: pd.DataFrame):

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

        cmap = colormaps.get_cmap('rainbow')

        scatter = ax.scatter(x, y, z, c=data, cmap=cmap, alpha=0.6)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        # Add a colorbar
        colorbar = fig.colorbar(scatter, ax=ax, label='Cluster ID')

        # Show the plot
        plt.show()

    # Customize the plot


def get_cluster_labels_from_df(df: pd.DataFrame) -> List[dict]:
    labels = []

    for (columnName, columnData) in df.items():
        str_col_name = str(columnName)

        if str_col_name.startswith(cluster_label_prefix):
            labels.append({
                'label': str_col_name,
                'num_clusters': max(columnData) + 1,
                'data': columnData
            })

    return labels


def compute_cluster_voxel_info(df: pd.DataFrame) -> List[pd.DataFrame]:
    """
    Computes the voxel information for each cluster

    :param df: The dataframe to perform quantitative analysis on
    :return: The voxel information for each cluster
    """

    print("This is the compute_cluster_voxel_info function! Doing some cool stuff now...")

    cluster_data_csv_path = input('Enter the path of the cluster data CSV file: ')

    if cluster_data_csv_path:
        df = pd.read_csv(cluster_data_csv_path, header=0, float_precision='high')

    new_den_c_path = input('Enter the path of the NewDenC.csv file: ') or 'data_files/NewDenC.csv'

    new_den_c = pd.read_csv(new_den_c_path, header=0, float_precision='high')

    cluster_labels = get_cluster_labels_from_df(df)

    voxel_info = []

    for i in range(len(cluster_labels)):

        new_df = {}

        cluster_label = cluster_labels[i]
        cluster_num = cluster_label.get('num_clusters')
        cluster_data = cluster_label.get('data')

        # there should be cluster_num rows in the new dataframe for each cluster

        new_df['cluster'] = [i for i in range(cluster_num)]

        print(f"Generating voxel info for cluster: {cluster_num}")

        # Get occurrences of each cluster
        occurrences = {}
        voxels = {}

        for j in range(len(cluster_data)):
            label = cluster_data[j]

            if label in occurrences:
                voxels[label].append(j)
                occurrences[label] += 1
            else:
                voxels[label] = [j]
                occurrences[label] = 1

        percentages = []
        voxel_counts = []

        for key in sorted(occurrences.keys()):
            voxel_counts.append(occurrences[key])
            percent = float(occurrences[key] / len(cluster_data) * 100)
            percentages.append(percent)
            # print(f"Cluster {key}: {percent}%")

        new_df['number of voxels'] = voxel_counts
        new_df['number of voxels (%)'] = percentages

        structure_ids = {}

        used_structure_ids = set()

        # for each cluster, get the list of structure ids that are in that cluster

        for key in voxels.keys():
            voxel_list = voxels[key]

            for voxel in voxel_list:
                structure_id = new_den_c.iloc[voxel]['Structure-ID']
                used_structure_ids.add(structure_id)

        for j in used_structure_ids:
            structure_ids[int(j)] = [0] * cluster_num

        for key in voxels.keys():
            voxel_list = voxels[key]

            structure_id_list = []

            for voxel in voxel_list:
                structure_id = new_den_c.iloc[voxel]['Structure-ID']
                structure_id_list.append(structure_id)

            structure_id_list_occurrences = {}

            for structure_id in structure_id_list:
                if structure_id in structure_id_list_occurrences:
                    structure_id_list_occurrences[structure_id] += 1
                else:
                    structure_id_list_occurrences[structure_id] = 1

            total_num_structure_ids = 0

            for struct_key in structure_id_list_occurrences.keys():
                total_num_structure_ids += structure_id_list_occurrences[struct_key]

            #print(f'\nCluster {key} structure id percentages: ')
            for struct_key in sorted(structure_id_list_occurrences.keys()):
                percent = float(structure_id_list_occurrences[struct_key] / total_num_structure_ids * 100)
                #print(f"Structure {struct_key}: {percent}%")

                structure_ids[int(struct_key)][key] = structure_id_list_occurrences[struct_key]
                
        for j in used_structure_ids:
            new_df[f'structure {int(j)}'] = structure_ids[int(j)]
            pass

        new_df = pd.DataFrame(new_df)

        print(new_df.head(n=min(13, cluster_num)))

        wants_to_save = input("Would you like to save the data frame to a CSV file? (y/n): ")

        if wants_to_save.lower() in ['y', 'yes', 'yeah', 'yep', 'yup']:
            name_of_file = input("What would you like to name the file?: ").replace(".csv", "")

            new_df.to_csv(f"{name_of_file}.csv", index=False)

            print(f"File saved as {name_of_file}.csv")

        # show the distributions of the structure ids for each cluster

        # for each cluster, get the pie chart of the structure ids




        voxel_info.append(new_df)

    print('Thanks for using the compute_cluster_voxel_info function! Have a nice day!')

    return voxel_info


def brain_kmeans():
    """
    STILL IN DEVELOPMENT
    Loads a CSV file based on a provided filepath and performs K-Means clustering based on the data frame contained

    :return: Cluster labels
    """

    # User greeting
    print("\nHey Colin! This is the ongoing development of brain_kmeans(). \nBooting up protocol now...")

    # Asking for filepath to be analyzed
    filepath = input("\nEnter file to be k-mean'ed: ")

    # Loading CSV file with pandas package
    df = pd.read_csv(filepath, header=0, float_precision='high')

    # Printing head table to ensure proper loading of data
    print(f"\nHEAD TABLE OF LOADED DATA FRAME: {filepath}")
    print(df.head())

    # Asking what cluster parameter/ID to label
    print("\nOf the 4 options: {4, 6, 8, 13}...")
    cluster_choice = input("How many clusters would you like to visualize?: ")
    if cluster_choice == '4':
        cluster_id = df['cluster_4']
    elif cluster_choice == '6':
        cluster_id = df['cluster_6']
    elif cluster_choice == '8':
        cluster_id = df['cluster_8']
    elif cluster_choice == '13':
        cluster_id = df['cluster_13']
    else:
        print("Invalid cluster choice. Play nice :( ")
        return

    # Extracting x, y, z coordinates
    x = df['X']
    y = df['Y']
    z = df['Z']

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot with colored points based on cluster_id
    scatter = ax.scatter(x, y, z, c=cluster_id, cmap='viridis')

    # Customize the plot
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # Add a colorbar
    colorbar = fig.colorbar(scatter, ax=ax, label='Cluster ID')

    # Show the plot
    plt.show()


def main():
    df = brain_kmeans_cbk()
    compute_cluster_voxel_info(df)


if __name__ == '__main__':
    main()
