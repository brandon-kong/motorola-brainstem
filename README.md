# Novel Brainstem Nuclei Localization

## Project Overview

The goal of this project is to identify and localize novel brainstem nuclei using a combination of gene expression data and spatial information. The data is derived from the Allen Mouse Brain Atlas (AMBA), which provides a comprehensive map of gene expression in the mouse brain. The data is organized into a 3D grid of voxels, each of which contains the expression levels of a set of genes. The goal is to use this data to identify clusters of voxels that correspond to distinct brainstem nuclei, and to identify the genes that are most strongly associated with each cluster.

## What is in this repository?

In **WhiteBoard.py**, there are two main functions:
- 'brain_kmeans_cbk' is a function that takes in the gene expression data and uses k-means clustering to identify clusters of voxels that correspond to distinct brainstem nuclei.
- 'compute_cluster_voxel_info' is a function that takes the clustered results and computes the composition of each cluster in terms of the Structure IDs within it.



## Getting Started

Here's how you can get this environment up and running on your local machine:

Clone the repository and step into it:

```bash
git clone https://github.com/brandon-kong/motorola-brainstem.git
cd motorola-brainstem
```

Then, create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

Windows
```bash
.venv/Scripts/activate
```

Unix
```bash
source .venv/bin/activate
```

Once activated, install all the dependencies to the environment
```bash
pip install -r requirements.txt
```

Now that all the dependencies are installed, you can run the code!

## Data

All data that I'm using will be in the `data_files` folder. I kindly ask that if you want to generate data from a function, that you set the file's location to be somewhere in `data_files/generated`, so it doesn't confuse users.
I'm working on documenting the data as well, so users know what the data means and what it represents in the context of our project.

## How to use?

You can start with running `WhiteBoard.py` since it contains the K-Means clustering code. I put the code that I want to execute in the `main` function at the bottom of `WhiteBoard.py`. Feel free to change it and comment things out.
You can try clustering on the datasets "output_K1.csv" with 4,6,8,13 clusters. You don't need to add any arguments to brain_kmeans_cbk(), it will all be input-based. 

## Whiteboard.py

There are 9 functions in WhiteBoard.py (not including the `main` function)

- `brain_kmeans_cbk()`
- `plot_knee_plot()`
- `plot_silhouette_plot()`
- `do_kmeans_clustering()`
- `plot_knee_plot()`
- `append_xyz_data_to_df()`
- `visualize_clusters()`
- `plot_xyz_scatter()`
- `plot_knee_plot()`
- `get_cluster_labels_from_df()`
- `compute_cluster_voxel_info()`
