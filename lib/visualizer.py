# Brandon Kong
# Motorola-Brainstem 2024

from matplotlib import pyplot as plt
import pandas as pd


def show_distributions(df: pd.DataFrame):
    # Plot the 13 structure ids

    structure_columns = df.columns[df.columns.str.startswith('structure')]
    structure_ids = df[structure_columns].stack().reset_index(drop=True)

    plt.hist(structure_ids, bins=20, alpha=0.5)
    plt.title("Distribution of Structure IDs")
    plt.xlabel("Structure ID")

    title = "Distribution of Data"
    x_label = "Value"
    y_label = "Frequency"

    plt.hist(df, bins=20, alpha=0.5)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def show_scatter(df: str, title: str, x_label: str, y_label: str):
    data_file = pd.read_csv(df, header=None, float_precision='high')
    df = pd.DataFrame(data_file)

    plt.scatter(df[0], df[1])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


