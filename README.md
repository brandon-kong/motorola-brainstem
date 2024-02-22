# Novel Brainstem Nuclei Localization

## Project Overview

The goal of this project is to identify and localize novel brainstem nuclei using a combination of gene expression data and spatial information. The data is derived from the Allen Mouse Brain Atlas (AMBA), which provides a comprehensive map of gene expression in the mouse brain. The data is organized into a 3D grid of voxels, each of which contains the expression levels of a set of genes. The goal is to use this data to identify clusters of voxels that correspond to distinct brainstem nuclei, and to identify the genes that are most strongly associated with each cluster.

## What is in this repository?

In **WhiteBoard.py**, there are two main functions:
- 'brain_kmeans_cbk' is a function that takes in the gene expression data and uses k-means clustering to identify clusters of voxels that correspond to distinct brainstem nuclei.
- 'compute_cluster_voxel_info' is a function that takes the clustered results and computes the composition of each cluster in terms of the Structure IDs within it.



