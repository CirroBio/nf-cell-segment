#!/usr/local/bin/python3

from anndata import AnnData
import scanpy as sc
import os
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def robust_scale(vals: pd.Series):
    """
    Scale the values in a Series using the interquartile range.
    """
    return (vals - vals.median()) / (vals.quantile(0.75) - vals.quantile(0.25))


def scale_intensities(
    df: pd.DataFrame,
    scaling: str,
    clip_lower: float,
    clip_upper: float
) -> pd.DataFrame:
    """
    Scale the intensities of the data in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to scale.
    scaling : str
        The scaling method to use. One of "robust", "zscore", "minmax", or "none".
    clip_lower : float
        The lower bound to clip the data to.
    clip_upper : float
        The upper bound to clip the data to.

    Returns
    -------
    pd.DataFrame
        The scaled data.
    """

    if scaling == "robust":
        logger.info("Scaling data using the robust method")
        df = df.apply(robust_scale)
    elif scaling == "zscore":
        logger.info("Scaling data using the Z-score method")
        df = df.apply(lambda col: (col - col.mean()) / col.std())
    elif scaling == "minmax":
        logger.info("Scaling data using the Min-Max method")
        df = df.apply(lambda col: (col - col.min()) / (col.max() - col.min()))
    elif scaling == "none":
        logger.info("No scaling applied")
    else:
        raise ValueError(f"Unknown scaling method: {scaling}")

    return df.clip(lower=clip_lower, upper=clip_upper)


def leiden(adata, resolution=1.0, n_neighbors=30):
    """
    Cluster the data using the Leiden algorithm.

    Parameters
    ----------
    adata : AnnData
        The annotated data object.
    resolution : float
        The resolution parameter for the Leiden algorithm.
    n_neighbors : int
        The number of neighbors to use for the KNN graph.
    """

    # Run the neighbors algorithm
    logger.info(f"Running the neighbors algorithm with {n_neighbors} neighbors")
    sc.pp.neighbors(
        adata,
        n_neighbors=n_neighbors,
        n_pcs=0
    )

    # Run the Leiden algorithm
    logger.info(f"Running the Leiden algorithm with resolution {resolution}")
    sc.tl.leiden(
        adata,
        resolution=resolution
    )

    # Run the UMAP algorithm
    logger.info("Running the UMAP algorithm")
    sc.tl.umap(adata)

    return adata


def make_summary_plots(adata):
    """
    Make summary plots of the clustering results using the scanpy library.
    These include:
        - A UMAP plot of the clusters
        - A dot plot of the cluster assignments

    Parameters
    ----------
    adata : AnnData
        The annotated data object.

    Output
    ------
    Files are written to *.pdf in the current working directory.
    """

    # Make a UMAP plot
    logger.info("Making a UMAP plot")
    sc.pl.umap(
        adata,
        color='leiden',
        add_outline=True,
        legend_loc="on data",
        legend_fontsize=12,
        legend_fontoutline=2,
        frameon=False,
        palette="Set1",
        save='.pdf'
    )

    # Make a dot plot
    logger.info("Making a dot plot")
    sc.pl.dotplot(adata, adata.var_names, groupby='leiden', save='.pdf')


def main():

    # Read the table with the measurement data
    fp = "${params.cluster_by}.csv"
    if not os.path.exists(fp):
        raise FileNotFoundError(f"Could not find file: {fp}")
    logger.info(f"Reading data from: {fp}")
    df = pd.read_csv(fp, index_col=0)

    # Scale the data as needed
    logger.info("Scaling the data")
    logger.info("scaling=${params.scaling}, clip_lower=${params.clip_lower}, clip_upper=${params.clip_upper}")
    df = scale_intensities(
        df,
        scaling="${params.scaling}",
        clip_lower=float("${params.clip_lower}"),
        clip_upper=float("${params.clip_upper}")
    )

    # Drop any columns which have NaN values
    logger.info("Dropping columns with NaN values")
    df = df.dropna(axis=1)
    assert df.shape[1] > 0, "No columns left after dropping NaN values"
    logger.info(f"Data now has {df.shape[1]:,} features")

    # Save the scaled data
    logger.info("Saving the scaled data")
    df.to_csv("scaled_data.csv")

    # Make an AnnData object
    logger.info("Creating an AnnData object")
    adata = AnnData(df)

    # Cluster the data
    logger.info("Clustering the data")
    logger.info("resolution=${params.cluster_resolution}, n_neighbors=${params.cluster_n_neighbors}")
    leiden(
        adata,
        resolution=float("${params.cluster_resolution}"),
        n_neighbors=int("${params.cluster_n_neighbors}")
    )

    # Write out the cluster assignments
    logger.info("Saving the cluster assignments")
    adata.obs.to_csv('leiden_clusters.csv')

    # Make summary plots
    logger.info("Making summary plots")
    make_summary_plots(adata)


main()
