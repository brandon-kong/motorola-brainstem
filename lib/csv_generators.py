# Brandon Kong's CSV Utility
# ML_Brainstem 2024


import pandas as pd

from lib.string_parse import string_to_int_list


def generate_dataframe_with_structure_id() -> dict[int, pd.DataFrame]:
    output_k1 = get_644_gene_dataframe()

    den_file_path = input("Enter the path to the NewDenC.csv file: ") or "data_files/NewDenC.csv"
    df = pd.read_csv(den_file_path, header=0, float_precision='high')

    structure_ids = (input("Enter the structure ids from this list (or press Enter to select all)\n"
                            "[136, 773, 970, 939, 1098, 235, 143, 978, 1107, 852, 661, 307, 1048]:"))

    if (structure_ids is None) or (structure_ids == ""):
        structure_ids = [136, 773, 970, 939, 1098, 235, 143, 978, 1107, 852, 661, 307, 1048]
    else:
        structure_ids = string_to_int_list(structure_ids)

    dataframes = {}

    list_to_save = []

    list_to_save_init = input("Which dataframes would you like to save? (Press Enter to skip):").strip()

    if (list_to_save_init is None) or (list_to_save_init == ""):
        list_to_save = []
    else:
        list_to_save = string_to_int_list(list_to_save_init)

    for structure_id in structure_ids:
        new_df = {}

        for column in df.columns:
            if column in output_k1.columns:
                new_df[column] = output_k1.get(column)
            elif column in ["Structure-ID", "X", "Y", "Z"]:
                new_df[column] = df.get(column)
            elif column == 'Unnamed: 0':
                new_df["voxel_number"] = df.get(column)

        data_frame = pd.DataFrame(new_df)

        data_frame = data_frame[data_frame["Structure-ID"] == structure_id]

        dataframes[structure_id] = data_frame

        print(data_frame.head())

        wants_to_save = structure_id in list_to_save

        if wants_to_save:
            name_of_file = input("What would you like to call this file?: ").replace(".csv", "")

            data_frame.to_csv(f"{name_of_file}.csv", index=False)

            print(f"File saved as {name_of_file}.csv")

    return dataframes


def get_644_gene_dataframe() -> pd.DataFrame:
    """
    :return:
    """

    file_path = input(
        "What is the path of the output_K1.csv file?\nDefault (data_files/output_K1.csv): ") or ("data_files"
                                                                                                 "/output_K1.csv")

    df = pd.read_csv(file_path, header=0, float_precision='high')
    new_df = {}

    for column in df.columns:
        new_df[column] = df.get(column)

    df = pd.DataFrame(new_df)

    return df


if __name__ == "__main__":
    data_frames = generate_dataframe_with_structure_id()

    for key in data_frames:
        brain_kmeans_cbk(data_frames[key])
