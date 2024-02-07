# Brandon Kong
# Motorola-Brainstem 2024

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

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

def show_pie(df: pd.DataFrame):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'A', 'B', 'C', 'D'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'B')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def show_stacked_bar_graph(quantitative_data_path: str):

    df = pd.read_csv(quantitative_data_path, float_precision='high')
    df = pd.DataFrame(df)

    clusters = df['cluster']

    structures = df.columns[df.columns.str.startswith('structure')]

    data = []

    for i in structures:
        data.append(df[i])

    data = np.array(data)

    fig, ax = plt.subplots()
    bottom = np.zeros(len(clusters))
    
    for i in range(len(structures)):
        ax.bar(clusters, data[i], label=structures[i])

    ax.set_ylabel('Number of Voxels')
    ax.set_title('Number of Voxels per Cluster')
    ax.legend(title='Structure ID')

    plt.tight_layout()
    plt.show()
    