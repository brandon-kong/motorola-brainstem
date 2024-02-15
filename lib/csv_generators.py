# Brandon Kong's CSV Utility
# ML_Brainstem 2024


import pandas as pd

# Generate a data frame with JUST the GAS-6


def get_gas_gene_data ():
    """
    :return:
    """

    file_path = input("What is the path of the output_K1.csv file?\nDefault (data_files/output_K1.csv): ") or "data_files/output_K1.csv"

    df = pd.read_csv(file_path, header=0, float_precision='high')
    new_df = {}

    new_df['Gas6-72008122'] = df['Gas6-72008122']

    df = pd.DataFrame(new_df)

    print("HEAD OF THE GAS6 GENE DATA: ")
    print(df.head())

    wants_to_save = input("Would you like to save this file? (y/n): ")

    if (wants_to_save.lower() in ['y', 'yes', 'yup']):

        name_of_file = input("What would you like to call this file?: ")

        df.to_csv(f"{name_of_file}.csv", index=False)

        print(f"File saved as {name_of_file}.csv")

    print("Thanks!")


def generate_dataframe_with_structure_id():
    output_k1 = get_644_gene_dataframe()

    den_file_path = input("Enter the path to the NewDenC.csv file: ") or "data_files/NewDenC.csv"
    df = pd.read_csv(den_file_path, header=0, float_precision='high')

    structure_id = int(input("Enter the structure id: "))

    new_df = {}

    # filter the dataframe to only include the rows where Structure-ID is equal to the structure id

    for column in df.columns:
        if column in output_k1.columns:
            new_df[column] = output_k1.get(column)
        elif column in ["Structure-ID", "X", "Y", "Z"]:
            new_df[column] = df.get(column)
        elif column == 'Unnamed: 0':
            new_df["voxel_number"] = df.get(column)

    data_frame = pd.DataFrame(new_df)

    data_frame = data_frame[data_frame["Structure-ID"] == structure_id]

    print(data_frame.head())

    wants_to_save = input("Would you like to save this file? (y/n): ")

    if (wants_to_save.lower() in ['y', 'yes', 'yup']):
        name_of_file = input("What would you like to call this file?: ").replace(".csv", "")

        data_frame.to_csv(f"{name_of_file}.csv", index=False)

        print(f"File saved as {name_of_file}.csv")



def get_644_gene_dataframe() -> pd.DataFrame:
    """
    :return:
    """

    file_path = input("What is the path of the output_K1.csv file?\nDefault (data_files/output_K1.csv): ") or "data_files/output_K1.csv"

    df = pd.read_csv(file_path, header=0, float_precision='high')
    new_df = {}

    for column in df.columns:
        new_df[column] = df.get(column)

    df = pd.DataFrame(new_df)

    return df

    
if __name__ == "__main__":
    generate_dataframe_with_structure_id()
