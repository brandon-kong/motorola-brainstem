# Brandon Kong's GenerateVoxelClusterIds
# Motorola_Brainstem 2024

from lib.string_parse import string_to_int_list
from WhiteBoard import generate_clustering_results
from typing import List
import typer


def generate_voxel_cluster_ids(file_path: str, cluster_num_list_arg: str):
    cluster_num_list = string_to_int_list(cluster_num_list_arg)

    for i in range(len(cluster_num_list)):
        clustering_results = generate_clustering_results(file_path, cluster_num_list[i])
        print("Clustering results for cluster number {}: {}".format(cluster_num_list[i], clustering_results))

    pass


if __name__ == '__main__':
    typer.run(generate_voxel_cluster_ids)
