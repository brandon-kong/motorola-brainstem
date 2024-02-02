# Brandon Kong's GenerateVoxelClusterIds
# Motorola_Brainstem 2024

from pprint import pprint
import pandas as pd

from lib.occurences import get_occurence_dict
from lib.string_parse import string_to_int_list

from WhiteBoard import generate_clustering_results
import typer


num_voxels = 1465


def generate_voxel_cluster_ids_data(
        input_data_file_path: str, 
        cluster_num_list_arg: str, 
        output_data_file_name: str
    ):
    """
    Generates a CSV file with the voxel number, cluster ids, 
    XYZ Coordinates, and gene densities
    
    :param file_path: The path to the file
    :param cluster_num_list_arg: A string of format "1,2,3" that 
    represents the cluster numbers

    :param output_data_file_path: The name of the output file

    :return: None
    """

    cluster_num_list = string_to_int_list(cluster_num_list_arg)

    df_data = {
        'voxel_number': []
    }

    for i in range(1, num_voxels + 1):
        df_data['voxel_number'].append(i)

    for i in range(len(cluster_num_list)):

        # Do the clustering from Colin's WhiteBoard.py, and get the results
        clustering_results = generate_clustering_results(input_data_file_path, cluster_num_list[i])

        df_data['{}_clusters'.format(cluster_num_list[i])] = clustering_results

        # Compute the occurences of each cluster group
        occurence_dict = get_occurence_dict(clustering_results)

        print(f"Occurence dictionary for cluster number {cluster_num_list[i]}: ")
        
        for key, value in occurence_dict.items():
            print(f"{key}: {value}")

    # Load the XYZ data from the mutated dataset
    
    xyz_dfs = pd.read_csv('data_files/output_K1_mutate.csv', header=0, float_precision='high')

    # Only add the X, Y, and Z columns to the df_data

    df_data['X'] = xyz_dfs['X']
    df_data['Y'] = xyz_dfs['Y']
    df_data['Z'] = xyz_dfs['Z']
    
    # Load the gene data from the original dataset
        
    gene_dfs = pd.read_csv('data_files/output_K1.csv', header=0, float_precision='high')

    # Iterate through each column and column data and add the gene data to the df_data

    for (columnName, columnData) in gene_dfs.items():
        df_data[columnName] = columnData

    df = pd.DataFrame(df_data)

    df.to_csv(f'data_files/generated/{output_data_file_name}.csv', index=False)

    print(f'Wrote dataframe to data_files/generated/{output_data_file_name}.csv')

if __name__ == '__main__':
    typer.run(generate_voxel_cluster_ids_data)
