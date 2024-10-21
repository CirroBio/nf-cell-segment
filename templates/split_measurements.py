import pandas as pd
import logging
from collections import defaultdict
from typing import Dict, Tuple

logger = logging.getLogger(str(__name__))


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
        spatial=["Centroid X µm", "Centroid Y µm"],
        attributes=["Object ID", "Detection probability", "Nucleus/Cell area ratio"]
    )

    # Use some flexible logic to assign data to categories, taking advantage of the
    # fact that the data is structured as "Partition: Measurement"
    for cname in df.columns.values:

        # Skip anything defined above
        if any([
            cname in cname_list
            for cname_list in struct.values()
        ]):
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
            _, partition, measurement = fields
            # Format the label as "Partition.Measurement"
            label = f"{partition}.{measurement}"
            # Pass through the name of the partition
            struct["partition"][label].append(cname)

    # Make the component tables
    partition = {
        partition: (
            df
            .reindex(columns=cnames)
            .rename(columns=lambda cname: cname.split(": ")[0])
        )
        for partition, cnames in struct["partition"].items()
    }
    spatial = df.reindex(columns=struct["spatial"])
    attributes = df.reindex(columns=struct["attributes"])

    return partition, spatial, attributes


if __name__ == "__main__":

    fp = "${measurements_csv}"
    partition, spatial, attributes = parse_stardist(fp)

    # Save to files
    for label, table in partition.items():
        table.to_csv(f"{label}.csv")

    spatial.to_csv("spatial.csv")
    attributes.to_csv("attributes.csv")
