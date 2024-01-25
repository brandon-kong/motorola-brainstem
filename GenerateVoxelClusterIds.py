# Brandon Kong's GenerateVoxelClusterIds
# Motorola_Brainstem 2024

import numpy as np
import pandas
import pandas as pd

from lib.string_parse import string_to_int_list
from WhiteBoard import generate_clustering_results
from typing import List
import typer


num_voxels = 1465


def generate_voxel_cluster_ids(file_path: str, cluster_num_list_arg: str):
    cluster_num_list = string_to_int_list(cluster_num_list_arg)

    df_data = {
        'voxel_number': []
    }

    for i in range(1, num_voxels + 1):
        df_data['voxel_number'].append(i)

    for i in range(len(cluster_num_list)):
        clustering_results = generate_clustering_results(file_path, cluster_num_list[i])
        print("Clustering results for cluster number {}: {}".format(cluster_num_list[i], clustering_results))

        df_data['{}_clusters'.format(cluster_num_list[i])] = clustering_results
        print("Clustering results for cluster number {}")

        # update the dataframe

    # load the genes
    gene_dfs = pd.read_csv('data_files/output_K1.csv', header=0, float_precision='high')

    # Iterate through each column and column data and add it to df_data

    for (columnName, columnData) in gene_dfs.items():
        df_data[columnName] = columnData

    df = pd.DataFrame(df_data)

    df.to_csv('data_files/generated/voxels_cluster_ids.csv', index=False)


if __name__ == '__main__':
    typer.run(generate_voxel_cluster_ids)
