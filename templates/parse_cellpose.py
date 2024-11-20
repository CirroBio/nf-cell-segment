#!/usr/bin/env python3

import gzip
import json
from typing import List
import numpy as np
import pandas as pd


def main():

    # fp = "${npy}"
    fp = "0bda515e370294ed94efd36bd53782288acacb040c171df2ed97fd691fc9d8fe_seg.npy"

    print(f"Loading {fp}")
    data = np.load(fp, allow_pickle=True).item()

    for kw, val in data.items():
        print(f"{kw}: {val}")

    # Convert the cells from the numpy array to GeoJSON format
    geojson = make_geojson(data["outlines"])

    # Save the GeoJSON to a gzip compressed JSON file
    with gzip.open("cells.geojson.gz", "wt") as f:
        json.dump(geojson, f)

    # Measure the intensity of each channel for each cell
    measurements = measure_intensity(data["img"], data["masks"])

    # Add the centroid coordinates to the measurements
    measurements = measurements.merge(
        find_centroids(data["masks"]),
        on="Object ID",
        how="left"
    )

    # Add in some dummy columns to conform to the expectations
    # from other methods
    measurements = measurements.assign(
        **{
            "Detection probability": 0,
            "Nucleus/Cell area ratio": 0
        }
    )

    # Write out to CSV
    measurements.to_csv("measurements.csv.gz", index=False)


def find_centroids(masks: np.ndarray) -> pd.DataFrame:
    
    # For each of the unique values in the masks, compute the centroid
    # of the cell
    centroids = []

    for cell_id in np.unique(masks):
        if cell_id == 0:
            continue

        # Create a mask for the cell
        cell_mask = masks == cell_id

        # Compute the centroid
        y, x = np.argwhere(cell_mask).mean(axis=0)

        centroids.append({
            "Object ID": cell_id,
            "Centroid X: pixels": x,
            "Centroid Y: pixels": y
        })

    centroids = pd.DataFrame(centroids)

    return centroids


def measure_intensity(img: np.ndarray, masks: np.ndarray) -> pd.DataFrame:

    # For each of the unique values in the masks, compute the
    # summary metrics for intensity each channel of the image
    measurements = []

    for cell_id in np.unique(masks):
        if cell_id == 0:
            continue
            
        # Create a mask for the cell
        cell_mask = masks == cell_id

        # Measure the intensity of each channel
        for channel in range(img.shape[0]):
            print(img.shape)
            intensity = img[channel, :, :].squeeze()[cell_mask]

            # Compute the summary statistics for the channel
            mean_intensity = np.mean(intensity)
            median_intensity = np.median(intensity)
            max_intensity = np.max(intensity)
            min_intensity = np.min(intensity)

            measurements.extend([
                {
                    "Object ID": cell_id,
                    "cname": f"Channel {channel}: Cell: {kw}",
                    "value": value
                }
                for kw, value in [
                    ["Mean", mean_intensity],
                    ["Median", median_intensity],
                    ["Max", max_intensity],
                    ["Min", min_intensity],
                ]
            ])

    measurements = pd.DataFrame(measurements)

    # Pivot to wide so that each row is a single cell
    measurements = measurements.pivot(
        index="Object ID",
        columns="cname",
        values="value"
    ).reset_index()

    return measurements


def make_geojson(outlines: np.ndarray) -> List[dict]:
    """
    Convert the outlines to GeoJSON format.

    The input `outlines` is an array of shape (w, h) where each pixel is assigned
    a unique integer value corresponding to the cell it belongs to.

    This function will convert the outlines to a list of GeoJSON features where each
    feature represents a cell.

    The GeoJSON format is as follows:
    {
        "type": "Feature",
        "cell": {
            "type": "Polygon",
            "coordinates": [[x1, y1], [x2, y2], ...]
        },
        "id": cell_id
    }

    This function will need to loop through each unique cell id and create a
    list of coordinates which describe the outline of the cell's shape.
    """

    geojson = []

    # Get the unique cell ids
    cell_ids = np.unique(outlines)

    for cell_id in cell_ids:
        # Skip 0 as it is the background
        if cell_id == 0:
            continue
    
        # Make a boolean mask of the cell
        cell_mask = outlines == cell_id

        # Get the coordinates of the cell outline
        coords = np.argwhere(cell_mask)

        # Trace the outline of the cell using those coordinates
        # This can be done by finding the next coordinate which is a neighbor
        # of the current coordinate
        # Start at the first coordinate
        outline = []
        current_coord = coords[0]
        outline.append(list(map(int, current_coord)))
        coords = np.delete(coords, 0, axis=0)
        while len(coords) > 0:
            # Compute the distance to all other coordinates
            distances = np.linalg.norm(coords - current_coord, axis=1)
            # Find the closest coordinate
            current_coord = coords[np.argmin(distances)]
            # Remove the coordinate from the list
            coords = np.delete(coords, np.argmin(distances), axis=0)
            # Add the coordinate to the list of coordinates
            outline.append(list(map(int, current_coord)))

        # Create the GeoJSON feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [outline]
            },
            "id": int(cell_id)
        }

        geojson.append(feature)

    return geojson


if __name__ == "__main__":
    main()
