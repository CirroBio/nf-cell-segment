process anndata {
    container "${params.container_spatialdata}"

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
    container "${params.container_spatialdata}"
    publishDir "${params.output_folder}", mode: 'copy', overwrite: true

    input:
    path anndata
    path cells_geo_json
    path image
    val pixel_size

    output:
    path "spatialdata.zarr.zip"

    script:
    template "spatialdata.py"
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