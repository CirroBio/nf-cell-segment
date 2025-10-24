# nf-cell-segment

Nextflow workflows for cell segmentation from high-resolution images using StarDist or Cellpose, with integrated visualization dashboards.

## Overview

This repository provides two Nextflow workflows for automated cell segmentation and analysis:

- **StarDist workflow** ([stardist.nf](stardist.nf)): Uses QuPath with StarDist for nucleus/cell detection
- **Cellpose workflow** ([cellpose.nf](cellpose.nf)): Uses Cellpose for cell segmentation

Both workflows support optional interactive dashboard generation to open and explore the segmentation results directly in Cirro.

## Features

- Cell segmentation using state-of-the-art deep learning models (StarDist or Cellpose)
- Automated measurement extraction (spatial coordinates, morphology, intensity)
- Optional Leiden clustering for cell type identification
- Interactive spatial visualization dashboards with Vitessce
- Containerized execution for reproducibility
- Support for high-resolution TIFF images

## Requirements

- [Nextflow](https://www.nextflow.io/) (version 20.04+)
- [Docker](https://www.docker.com/) or [Singularity](https://sylabs.io/singularity/)
- Input: High-resolution TIFF image
- For StarDist: Pre-trained StarDist model file

## Quick Start

### StarDist Workflow

```bash
nextflow run stardist.nf \
  --input_tiff /path/to/image.tiff \
  --output_folder /path/to/output \
  --model /path/to/stardist_model.pb \
  --channels 0 \
  --cellExpansion 5.0
```

### Cellpose Workflow

```bash
nextflow run cellpose.nf \
  --input_tiff /path/to/image.tiff \
  --output_folder /path/to/output \
  --pretrained_model cyto3 \
  --diameter 0
```

## Parameters

### Common Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `input_tiff` | Yes | - | Path to input TIFF image |
| `output_folder` | Yes | - | Directory for output files |
| `build_dashboard` | No | `true` | Generate interactive visualization dashboard |

### StarDist-Specific Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `model` | Yes | - | Path to StarDist model file (.pb) |
| `threshold` | No | `0.5` | Detection threshold |
| `channels` | No | `0` | Channel index to use for segmentation |
| `cellExpansion` | No | `5.0` | Cell boundary expansion (μm) |
| `cellConstrainScale` | No | `1.5` | Cell expansion constraint scale |
| `minPercentileNormalization` | No | `1` | Minimum percentile for normalization |
| `maxPercentileNormalization` | No | `99` | Maximum percentile for normalization |
| `container_stardist` | No | `public.ecr.aws/cirrobio/qupath:v0.6.0` | Docker container for QuPath/StarDist |

### Cellpose-Specific Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `pretrained_model` | No | `cyto3` | Cellpose pretrained model name |
| `channel_axis` | No | `0` | Axis of image containing channels |
| `segment_channel` | No | `0` | Channel to use for segmentation |
| `diameter` | No | `0` | Expected cell diameter (0 = auto-estimate) |
| `flow_threshold` | No | `0.4` | Flow error threshold |
| `cellprob_threshold` | No | `0` | Cell probability threshold |
| `no_resample` | No | `false` | Disable resampling |
| `exclude_on_edges` | No | `false` | Exclude cells on image edges |
| `z_axis` | No | `false` | Axis of image containing Z dimension |
| `nuclear_channel` | No | `false` | Nuclear channel index |
| `anisotropy` | No | `false` | Anisotropy value for 3D images |
| `container_cellpose` | No | `public.ecr.aws/cirrobio/cellpose:3.1.0` | Docker container for Cellpose |

### Dashboard/Clustering Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `cluster_by` | `Cell.Mean` | Feature prefix to use for clustering |
| `cluster_method` | `leiden` | Clustering method |
| `cluster_resolution` | `1.0` | Leiden clustering resolution |
| `cluster_n_neighbors` | `10` | Number of neighbors for graph construction |
| `scaling` | `robust` | Scaling method: `none`, `zscore`, `robust`, `minmax` |
| `clip_lower` | `-2.0` | Lower bound for clipping scaled values |
| `clip_upper` | `2.0` | Upper bound for clipping scaled values |
| `instance_key` | `object_id` | Column name for cell instance IDs |
| `container_python` | `public.ecr.aws/cirrobio/python-utils:e3e173f` | Docker container for Python utilities |

## Output Files

The workflows generate the following outputs:

### StarDist Output (`output_folder/stardist/`)
- `measurements.csv.gz`: Cell measurements and features
- `cells.geo.json.gz`: Cell boundaries in GeoJSON format
- `qupath_project/`: QuPath project directory

### Cellpose Output (`output_folder/cellpose/`)
- Similar structure with Cellpose-specific results

### Dashboard Output (`output_folder/dashboard/`)
- `spatialdata.zarr.zip`: Spatial data in Zarr format
- `*.vt.json`: Vitessce configuration file for interactive visualization in Cirro

### Clustering Output (`output_folder/cell_clustering/`)
- `leiden_clusters.csv`: Cluster assignments
- `scaled_intensities.csv`: Scaled feature intensities
- `figures/`: Visualization plots (UMAP, clustering results)
