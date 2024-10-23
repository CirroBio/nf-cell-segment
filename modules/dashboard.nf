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
    publishDir "${params.output_folder}", mode: 'copy', overwrite: true

    input:
    path anndata
    path cells_geo_json
    path image
    val pixel_size

    output:
    path "spatialdata.zarr.zip"
    path "spatialdata.vt.json"

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
}