process anndata {
    container "${params.container_python}"

    input:
    path spatial
    path attributes
    path clusters
    path intensities

    output:
    path "spatialdata.h5ad"

    script:
    template "make_anndata.py"
}


process spatialdata {
    container "${params.container_python}"
    publishDir "${params.output_folder}/dashboard", mode: 'copy', overwrite: true, pattern: "*.zarr.zip"

    input:
    path anndata
    path cells_geo_json
    path image
    val pixel_size

    output:
    path "spatialdata.zarr.zip", emit: zarr_zip
    path "spatialdata.kwargs.json", emit: kwargs

    """#!/bin/bash
spatialdata.py \
    --anndata "${anndata}" \
    --cells_geo_json "${cells_geo_json}" \
    --image "${image}" \
    --pixel_size "${pixel_size}"

# Zip up the output
echo "Zipping up the output"
zip -r spatialdata.zarr.zip spatialdata.zarr
rm -rf spatialdata.zarr
    """
}


process configure_vitessce {
    container "${params.container_python}"
    publishDir "${params.output_folder}/dashboard", mode: 'copy', overwrite: true

    input:
    path "spatialdata.kwargs.json"

    output:
    path "spatialdata.vt.json"

    """#!/bin/bash
set -e
configure_vitessce.py
"""
}


workflow dashboard {
    
    take:
    spatial
    attributes
    clusters
    intensities
    cells_geo_json
    image
    pixel_size

    main:
    anndata(
        spatial,
        attributes,
        clusters,
        intensities
    )

    spatialdata(
        anndata.out,
        cells_geo_json,
        image,
        pixel_size
    )

    configure_vitessce(
        spatialdata.out.kwargs
    )
}