# Novel Brainstem Nuclei Localization

## Project Overview

The goal of this project is to identify and localize novel brainstem nuclei using a combination of gene expression data and spatial information. The data is derived from the Allen Mouse Brain Atlas (AMBA), which provides a comprehensive map of gene expression in the mouse brain. The data is organized into a 3D grid of voxels, each of which contains the expression levels of a set of genes. The goal is to use this data to identify clusters of voxels that correspond to distinct brainstem nuclei, and to identify the genes that are most strongly associated with each cluster.

## To-Do List

- [ ] Prepare DEN 193-gene “complete” data frame [0.01] and perform a similar clustering analysis

- [ ] Create an INT “sister” data frame, based on the 644-gene “complete” data frame [0.001]

- [ ] Rotate ”output_K1.csv” data and fine tune brain_hac() accordingly, to project clusters of voxels instead of genes. Then project voxel clusters onto a 3-D space

- [x] Generate pie charts and bar graphs for chat-252 cluster results

- [x] Incorporate a total voxel count for per cluster in pie chart

- [x] Improve upon color gradient for stacked bar graphs

- [ ] Update brainscan() to display histogram specific to chat-252’s gene expression distribution

- [ ] Plot/identify initial centroids of each cluster for later comparison

- [x] Implement sub-clustering routine into brain_k-means_cbk() to cluster within specified cluster(s) and pinpoint Structure-IDs within each

- [ ] Update on Project Overview for quarterly progress report and later reference (edited) 
