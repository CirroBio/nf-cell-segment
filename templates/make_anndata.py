#!/usr/local/bin/python3

import pandas as pd
from anndata import AnnData
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def read_csv(fp: str, label: str) -> pd.DataFrame:
    """
    Read a CSV file and log the number of objects read.
    """
    logger.info(f"Reading in {label} from {fp}")
    df = pd.read_csv(fp, index_col=0)
    logger.info(f"Read in data for {df.shape[0]:,} objects and {df.shape[1]:,} features")
    return df


def sanitize_cnames(cname: str) -> str:
    """
    Sanitize column names to snakecase.
    """
    cname = (
        cname
        .lower()
        .replace(" ", "_")
        .replace(".", "_")
    )
    while "__" in cname:
        cname = cname.replace("__", "_")

    return cname


def main(
    spatial = "${spatial}",
    attributes = "${attributes}",
    clusters = "${clusters}",
    intensities = "${intensities}"
):
    spatial = read_csv(spatial, "spatial data")
    attributes = read_csv(attributes, "attributes")
    clusters = read_csv(clusters, "clusters")
    intensities = read_csv(intensities, "intensities")

    # The index for all tables must be the same
    logger.info("Checking that all tables have the same index")
    assert spatial.index.equals(attributes.index)
    assert spatial.index.equals(clusters.index)
    assert spatial.index.equals(intensities.index)

    # Add the cluster data to the attributes
    logger.info("Merging cluster data with attributes")
    obs = attributes.merge(clusters, left_index=True, right_index=True)

    # The columns of obs will be sanitized to snakecase
    # Note that "Object ID" will be renamed to "object_id"
    obs = obs.rename(columns=sanitize_cnames)

    # Create the AnnData object
    logger.info("Creating AnnData object")
    adata = AnnData(
        X=intensities,
        obs=obs,
        obsm={"spatial": spatial.values}
    )

    # Save to disk
    logger.info("Saving data to spatialdata.h5ad")
    adata.write("spatialdata.h5ad")


main()