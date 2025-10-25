#!/usr/local/bin/python3
from pathlib import Path

import pandas as pd
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def pick_cname(cnames: List[str], prefix: str):
    for cname in cnames:
        if cname.startswith(prefix):
            return cname


def parse_stardist(fp: str) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    """
    Parse a table of data output by StarDist into a dict of component tables.

    Parameters
    ----------
    fp : str
        The file path to the table.

    Returns
    -------
    partition : dict
        The partitioned data.
    attributes : pd.DataFrame
        The attributes of the objects.
    spatial : pd.DataFrame
        The spatial data.
    """

    # Read the table
    df = pd.read_csv(fp)
    logger.info(f"Read in data for {df.shape[0]:,} objects")

    # To start, define where the single-field columns should be assigned
    struct = dict(
        partition=defaultdict(list), # This will be populated with keys like "Cell.Mean", "Membrane.Min", etc.
        spatial=[pick_cname(df.columns.values, prefix) for prefix in ["Centroid X", "Centroid Y"]],
        attributes=["Object ID", "Detection probability", "Nucleus/Cell area ratio"]
    )
    expected_cnames = [cname for cname_list in struct.values() for cname in cname_list ]

    # Make sure that all of the expected columns are present
    for cname in expected_cnames:
        if not cname in df.columns.values:
            raise ValueError(f"Missing column: {cname}")

    # Use some flexible logic to assign data to categories, taking advantage of the
    # fact that the data is structured as "Partition: Measurement"
    for cname in df.columns.values:

        # Skip columns which have already been set up
        if cname in expected_cnames:
            continue

        # Parse the column names into fields
        fields = cname.split(": ")

        # Cell attributes
        # e.g. Nucleus: Area µm^2
        if len(fields) == 2:
            struct["attributes"].append(cname)

        # Measured intensities
        # e.g. DAPI: Nucleus: Mean
        elif len(fields) == 3:
            partition, _, measurement = fields
            # Format the label as "Partition.Measurement"
            label = f"{partition}.{measurement}"
            # Pass through the name of the partition
            struct["partition"][label].append(cname)
            logger.info(f"Assigned {cname} to {label}")

    # Make the component tables
    partition = {
        partition: (
            df
            .reindex(columns=cnames)
            .rename(columns=lambda cname: cname.split(": ")[1])
        )
        for partition, cnames in struct["partition"].items()
    }
    spatial = df.reindex(columns=struct["spatial"])
    attributes = df.reindex(columns=struct["attributes"])

    return partition, spatial, attributes


def main():

    fp = Path("~/Downloads/measurements.csv").expanduser()
    logger.info(f"Reading data from: {fp}")
    partition, spatial, attributes = parse_stardist(fp)

    # Save to files
    for label, table in partition.items():
        logger.info(f"Saving {label} data")
        table.to_csv(f"{label}.csv")

    logger.info("Saving spatial data")
    spatial.to_csv("spatial.csv")
    logger.info("Saving attributes data")
    attributes.to_csv("attributes.csv")


main()
