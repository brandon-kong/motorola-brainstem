# Colin's Whiteboard
# ML_Brainstem 2024

# Loading global packages
from typing import List, Optional
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

from pathlib import Path

from lib.visualizer import show_stacked_bar_graph

# Local packages

# Choosing a matplotlib backend to ensure plot pop-up will deploy
import matplotlib
from matplotlib import colormaps

from lib.csv_generators import generate_dataframe_with_structure_id

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


###################################################################################################################


def brain_kmeans_cbk(
        df: Optional[pd.DataFrame] = None,
        voxel_numbers: Optional[pd.Series] = None,
        is_subcluster: Optional[bool] = False,
        cluster_id: Optional[int] = None,

) -> pd.DataFrame:
    """
    Loads a CSV file based on a provided filepath and performs K-Means clustering based on the data frame contained

    :param df: The dataframe to perform K-Means clustering on
    :param voxel_numbers: The list of voxel numbers to append to the dataframe
    :param is_subcluster: Whether the clustering is a subcluster
    :param cluster_id: The cluster id to subcluster

    :return: The dataframe generated with the cluster ids, XYZ, and the genes
    """

    # User greeting
    name = input("What is your name? ")
    print(f"\nHey {name}! This is brain_kmeans_cbk(). Doing some cool stuff now...")

    # Asking for filepath to be analyzed

    new_df = {}

    if df is None:
        filepath = input("\nEnter file to be k-mean'ed: ")

        # Loading CSV file with pandas package
        df = pd.read_csv(filepath, header=0, float_precision='high')
    else:
        print("Dataframe provided, skipping file load.")

    new_df['voxel_number'] = [i+1 for i in range(len(df))]

    removed_columns = {}

    for (columnName, columnData) in df.items():
        if columnName in ['X', 'Y', 'Z', 'Structure-ID', 'voxel_number', 'Unnamed: 0']:
            new_df[columnName] = columnData
            removed_columns[columnName] = columnData
            df.drop(columnName, axis=1, inplace=True)

    # Printing head table to ensure proper loading of data
    print(f"\nHead table of the loaded dataframe:")
    print(df.head())

    # Asking for a max number of clusters
    max_clusters = (input("\nEnter the maximum number of k-means clusters: "))

    while not max_clusters or not max_clusters.isdigit():
        print("Invalid input. Please enter a valid number.")
        max_clusters = (input("\nEnter the maximum number of k-means clusters: "))

    max_clusters = int(max_clusters)

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
    # plt.show(block=False)

    # Asking user for the number of clusters they would like to set for clustering protocol
    cluster_set = input("\nEnter the number of clusters you would like to set for clustering protocol: ")

    while not cluster_set:
        print("Invalid input. Please enter a valid number.")
        cluster_set = input("\nEnter the number of clusters you would like to set for clustering protocol: ")

    cluster_set = string_to_int_list(cluster_set)

    # Performing k-means

    cluster_results: List[List[int]] = []

    for i in range(len(cluster_set)):
        cluster_labels = do_kmeans_clustering(df, cluster_set[i])

        if len(cluster_labels) == 0:
            print("No clusters generated. Exiting...")
            continue

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

        # print(f"\nCluster Occurrences for {cluster_set[i]} clusters: {occurrences}")

    # Load the XYZ data from the mutated dataset

    # first, see if removed_columns has the XYZ data in it

    xyz_dfs = pd.read_csv('data_files/NewDenC.csv', header=0, float_precision='high')

    # Add all the gene data to the df_data

    # if voxel_numbers is defined, we should only add rows that are in the voxel_numbers list

    if voxel_numbers is not None:
        new_df['voxel_number'] = voxel_numbers

    if 'voxel_number' in removed_columns:
        new_df['voxel_number'] = removed_columns['voxel_number']

    for (columnName, columnData) in xyz_dfs.items():
        if (columnName in df) or columnName in ['X', 'Y', 'Z']:
            # filter column data to only include the rows that are in the voxel_numbers list
            if voxel_numbers is not None:
                new_df[columnName] = [columnData[i] for i in range(len(columnData)) if i in voxel_numbers]
            else:
                # see if the column name is in the removed columns
                if columnName in removed_columns:
                    new_df[columnName] = removed_columns[columnName]
                else:
                    new_df[columnName] = columnData

    # Add the focused genes to the df_data as well

    for (columnName, columnData) in df.items():
        if columnName in df:
            new_df[columnName] = columnData

    df = pd.DataFrame(new_df)

    print(df.head())

    # Visualize the clusters
    title = "Cluster label for label"

    if is_subcluster:
        title = f"Subcluster on cluster {cluster_id} for label"

    visualize_clusters(df, title=title)

    wants_to_save = input("Would you like to save the data frame to a CSV file? (y/n): ")

    if wants_to_save.lower() in ['y', 'yes', 'yeah', 'yep', 'yup']:
        name_of_file = input("What would you like to name the file?: ").replace(".csv", "")

        # create the directory if it doesn't exist

        # get the path of the file without the file name
        file_path = Path(name_of_file)
        directory = file_path.parent

        # create the directory if it doesn't exist
        directory.mkdir(parents=True, exist_ok=True)

        df.to_csv(f"{name_of_file}.csv", index=False)

        print(f"File saved as {name_of_file}.csv")

    print(f"Have a nice day, {name}!")

    # Returning the list of cluster results
    return df, name


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


def do_kmeans_clustering(df: pd.DataFrame, n_clusters: int) -> List[int]:
    """
    Performs K-Means clustering on a given data frame

    :param df: The data frame to perform K-Means clustering on
    :param n_clusters: The number of clusters to generate
    :return: Cluster labels
    """

    # get the length of the dataframe rows without the header

    df_len = df.shape[0]

    if df_len < n_clusters:
        print(f"Number of clusters requested is greater than the number of rows in the dataframe. "
              f"Please enter a number less than {df_len}")
        return []

    kmeans: KMeans = KMeans(n_clusters=n_clusters, random_state=25)
    cluster_labels: List[int] = kmeans.fit_predict(df)

    return cluster_labels


def append_xyz_data_to_df(df: pd.DataFrame, voxel_numbers: pd.Series | None = None) -> pd.DataFrame:
    """
    Appends the XYZ data from the mutated dataset to the given dataframe

    :param df: The dataframe to append the XYZ data to
    :param voxel_numbers: The list of voxel numbers to append to the dataframe
    :return: The dataframe with the appended XYZ data
    """

    new_df = {}

    # Load the XYZ data from the mutated dataset
    xyz_dfs = pd.read_csv('data_files/NewDenC.csv', header=0, float_precision='high')

    # if voxel_numbers is defined, we should only add rows that are in the voxel_numbers list
    if voxel_numbers is not None:
        new_df['voxel_number'] = voxel_numbers

    for (columnName, columnData) in xyz_dfs.items():
        if (columnName in df) or columnName in ['X', 'Y', 'Z']:
            # filter column data to only include the rows that are in the voxel_numbers list
            if voxel_numbers is not None:
                new_df[columnName] = [columnData[i] for i in range(len(columnData)) if i in voxel_numbers]
            else:
                new_df[columnName] = columnData

    # Add all the gene data to the df_data

    for (columnName, columnData) in df.items():
        if columnName in df:
            new_df[columnName] = columnData

    df = pd.DataFrame(new_df)

    return df


def visualize_clusters(df: pd.DataFrame, title: str = "Cluster label for label"):
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

        ax.set_title(title + f" {label}")

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


def plot_xyz_scatter(df: pd.DataFrame, title: str = "XYZ Scatter Plot"):
    """
    Plots the XYZ scatter plot for the given dataframe

    :param df: The dataframe to plot the XYZ scatter plot for
    :return:
    """

    x = df['X']
    y = df['Y']
    z = df['Z']

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot with colored points based on cluster_id
    scatter = ax.scatter(x, y, z)

    # Customize the plot
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.set_title(title)

    # Show the plot
    plt.show()


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


def compute_cluster_voxel_info(df: pd.DataFrame | None, name: str = "") -> List[pd.DataFrame]:
    """
    Computes cluster compositions for each cluster including
    - Number of voxels in each cluster
    - Number of voxels as a percentage of the total number of voxels in the cluster
    - Structure IDs and how many voxels are in all 13 structure IDs for each cluster

    :param df: The dataframe to perform quantitative analysis on
    :param name: The name of the user
    :return: A list of dataframes containing the voxel information for each number of clusters
    """

    print("This is the compute_cluster_voxel_info function! Doing some cool stuff now...")

    cluster_data_csv_path = input('Enter the path of the cluster data CSV file: ')

    if cluster_data_csv_path:
        df = pd.read_csv(cluster_data_csv_path, header=0, float_precision='high' )

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
                structure_id = df.iloc[voxel].get('Structure-ID') or new_den_c.iloc[voxel]['Structure-ID']

                used_structure_ids.add(structure_id)

        for j in used_structure_ids:
            structure_ids[int(j)] = [0] * cluster_num

        for key in voxels.keys():
            voxel_list = voxels[key]

            structure_id_list = []

            for voxel in voxel_list:
                structure_id = df.iloc[voxel].get('Structure-ID') or new_den_c.iloc[voxel]['Structure-ID']
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

            for struct_key in sorted(structure_id_list_occurrences.keys()):
                percent = float(structure_id_list_occurrences[struct_key] / total_num_structure_ids * 100)

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

    print(f'Thanks for using the compute_cluster_voxel_info function! Have a nice day, {name}!')

    return voxel_info


def main():
    # df, name = brain_kmeans_cbk()
    # compute_cluster_voxel_info(df=None, name="Colin")

    visualize_clusters(pd.read_csv("data_files/generated/voxels_cluster_ids.csv"), "Cluster label for label")


if __name__ == '__main__':
    main()
