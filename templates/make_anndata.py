#!/usr/bin/env python3

import pandas as pd
from anndata import AnnData
import logging

logger = logging.getLogger(str(__name__))


def read_csv(fp: str, label: str) -> pd.DataFrame:
    """
    Read a CSV file and log the number of objects read.
    """
    logger.info(f"Reading in {label} from {fp}")
    df = pd.read_csv(fp, index_col=0)
    logger.info(f"Read in data for {df.shape[0]:,} objects and {df.shape[1]:,} features")
    return df


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

    # Create the AnnData object
    logger.info("Creating AnnData object")
    adata = AnnData(
        X=intensities.values,
        obs=obs,
        obsm={"spatial": spatial.values}
    )

    # Save to disk
    logger.info("Saving data to spatialdata.h5ad")
    adata.write("spatialdata.h5ad")


if __name__ == "__main__":
    main()