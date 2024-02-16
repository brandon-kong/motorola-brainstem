import pandas as pd

from WhiteBoard import cluster_label_prefix, brain_kmeans_cbk, append_xyz_data_to_df, plot_xyz_scatter

def generate_cluster_id_subcluster_dataframe_from_file() -> tuple[pd.DataFrame, int, str]: 
    """
    Generates a dataframe from a file containing the clustered results
    which can then be used to subcluster a cluster from the dataset

    :return: A tuple containing the dataframe, the cluster id, and the cluster label
    """
    file_path = input("Enter the path to the dataset with clustered results: ") or ("data_files/generated"
                                                                                    "/voxels_cluster_ids.csv")
    df = pd.read_csv(file_path, header=0, float_precision='high')

    cluster_label = input("Enter the number of the cluster you want to subcluster: ")
    int_cluster_label = int(cluster_label)

    cluster_label = cluster_label_prefix + cluster_label

    while cluster_label not in df.columns:
        print(f"Cluster {cluster_label} not found")
        cluster_label = input("Enter the number of the cluster you want to subcluster: ")
        int_cluster_label = int(cluster_label)
        cluster_label = cluster_label_prefix + cluster_label

    subcluster = df.get(cluster_label)

    int_which_cluster_id = -1

    while int_which_cluster_id < 0 or int_which_cluster_id >= int_cluster_label:
        which_cluster_id = input(f"From the {int_cluster_label} cluster{'' if int_cluster_label == 1 else 's'}, which "
                                 f"cluster ID do you want to subcluster (0-{int_cluster_label - 1})? ")
        int_which_cluster_id = int(which_cluster_id)

        if (int_which_cluster_id is None) or int_which_cluster_id < 0 or int_which_cluster_id >= int_cluster_label:
            print("Invalid cluster id")
            continue

    # create a dataframe with only the rows that have the cluster id
    new_df = {}

    for column in df.columns:
        if (not column.startswith(cluster_label_prefix)) and (column not in ["X", "Y", "Z"]):
            new_df[column] = df.get(column)

    new_df[cluster_label] = subcluster

    data_frame = pd.DataFrame(new_df)

    # filter the dataframe to only include the rows with the cluster id

    subcluster = data_frame[data_frame[cluster_label] == int_which_cluster_id]

    # remove the cluster id column

    subcluster = subcluster.drop(cluster_label, axis=1)

    print(subcluster.head())

    return subcluster, int_which_cluster_id, cluster_label


def brain_ception():
    """
    Subclusters a cluster from a dataset containing clustered results

    :return: None
    """

    print("We need to go deeper.")

    data_frame, cluster_id, cluster_num = generate_cluster_id_subcluster_dataframe_from_file()

    # temporarily take out voxel_number to ensure clustering works on only gene expression data
    voxel_number = data_frame.get("voxel_number")

    data_frame = data_frame.drop("voxel_number", axis=1)

    xyz_data = append_xyz_data_to_df(data_frame, voxel_number)

    print(xyz_data.head())
    plot_xyz_scatter(xyz_data, f"Subclustering of {cluster_num}'s cluster {cluster_id}")

    # cluster the data

    try:
        cluster_labels = brain_kmeans_cbk(data_frame, voxel_number, is_subcluster=True, cluster_id=cluster_id)
    except:
        print("Clustering failed")



if __name__ == '__main__':
    brain_ception()

# data_files/generated/chat252/chat252_clustered_xyz.csv