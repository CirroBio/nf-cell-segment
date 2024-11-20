include { split_measurements } from './shared.nf'

process find_cells {
    container "${params.container_cellpose}"
    publishDir "${params.output_folder}/cellpose", mode: 'copy', overwrite: true

    input:
    path "inputs/"

    output:
    path "*.npy", emit: npy
    path "*.tif", emit: tif
    path "*.png", emit: png

    script:
    template "cellpose.sh"
}

process measure_cells {
    container "${params.container_python}"
    publishDir "${params.output_folder}/cellpose", mode: 'copy', overwrite: true

    input:
    path npy

    output:
    path "cells.geojson.gz", emit: cells_geo_json
    path "measurements.csv.gz", emit: measurements_csv

    script:
    template "parse_cellpose.py"
}

process mock_pixel_size {
    container "${params.container_python}"
    publishDir "${params.output_folder}/cellpose", mode: 'copy', overwrite: true

    output:
    path "pixelWidth"

    script:
    """#!/bin/bash
echo "1.0" > pixelWidth
    """
}

workflow cellpose {
    take:
    input_tiff

    main:
    // Run cellpose to find cells
    find_cells(input_tiff)

    // Parse the cell shapes from .npy format
    measure_cells(find_cells.out.npy)

    // Parse out the spatial and attribute information
    split_measurements(measure_cells.out.measurements_csv)

    // Mock the pixel size
    mock_pixel_size()

    emit:
    cells_geo_json = measure_cells.out.cells_geo_json
    spatial = split_measurements.out.spatial
    attributes = split_measurements.out.attributes
    intensities = split_measurements.out.intensities
    pixel_size = mock_pixel_size.out
}