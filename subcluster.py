import pandas as pd

from WhiteBoard import cluster_label_prefix, do_kmeans_clustering, brain_kmeans_cbk

from lib.string_parse import string_to_int_list

def generate_cluster_id_subcluster_dataframe_from_file() -> pd.DataFrame:
    file_path = input("Enter the path to the dataset with clustered results: ") or ("data_files/generated"
                                                                                    "/voxels_cluster_ids.csv")
    df = pd.read_csv(file_path, header=0, float_precision='high')

    cluster_label = input("Enter the number of the cluster you want to subcluster: ")
    int_cluster_label = int(cluster_label)

    cluster_label = cluster_label_prefix + cluster_label

    subcluster = df.get(cluster_label)

    int_which_cluster_id = -1

    while int_which_cluster_id < 0 or int_which_cluster_id >= int_cluster_label:
        which_cluster_id = input(f"From the {int_cluster_label} cluster{'' if int_cluster_label == 1 else 's'}, which "
                                 f"cluster ID do you want to subcluster (0-{int_cluster_label - 1})? ")
        int_which_cluster_id = int(which_cluster_id)

        if (not int_which_cluster_id) or int_which_cluster_id < 0 or int_which_cluster_id >= int_cluster_label:
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

    return subcluster


def brain_ception():
    print("We need to go deeper.")

    data_frame = generate_cluster_id_subcluster_dataframe_from_file()

    # temporarily take out voxel_number to ensure clustering works on only gene expression data
    voxel_number = data_frame.get("voxel_number")

    for i in voxel_number:
        print(i)

    data_frame = data_frame.drop("voxel_number", axis=1)

    # cluster the data

    cluster_labels = brain_kmeans_cbk(data_frame, voxel_number)

    # put the voxel_number back in


if __name__ == '__main__':
    brain_ception()
