import pandas as pd

from WhiteBoard import cluster_label_prefix

def subcluster_from_file():
    file_path = input("Enter the path to the dataset with clustered results: ")
    df = pd.read_csv(file_path, header=0, float_precision='high')

    cluster_label = input("Enter the number of the cluster you want to subcluster: ")
    int_cluster_label = int(cluster_label)

    cluster_label = cluster_label_prefix + cluster_label

    subcluster = df.get(cluster_label)

    int_which_cluster_id = -1

    while int_which_cluster_id < 0 or int_which_cluster_id > int_cluster_label:
        which_cluster_id = input(f"From the {int_cluster_label} cluster{'' if int_cluster_label == 1 else 's'}, which one do you want to subcluster? ")
        int_which_cluster_id = int(which_cluster_id)

        if (not int_which_cluster_id) or int_which_cluster_id < 0 or int_which_cluster_id > int_cluster_label:
            print("Invalid cluster id")
            continue

    return subcluster

if __name__ == '__main__':
    subcluster_from_file()