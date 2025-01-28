process leiden {
    container "${params.container_python}"
    publishDir "${params.output_folder}/cell_clustering", mode: 'copy', overwrite: true

    input:
    path "*"

    output:
    path "leiden_clusters.csv", emit: clusters
    path "scaled_intensities.csv", emit: scaled_intensities
    path "figures/*.p*", emit: plots

    script:
    template "leiden.py"

}

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
    path pixel_size

    output:
    path "spatialdata.zarr.zip", emit: zarr_zip
    path "spatialdata.kwargs.json", emit: kwargs

    script:
    template "spatialdata.py"
}


process configure_vitessce {
    container "${params.container_python}"
    publishDir "${params.output_folder}/dashboard", mode: 'copy', overwrite: true

    input:
    path "spatialdata.kwargs.json"

    output:
    path "*.vt.json"

    script:
    template "configure_vitessce.py"
}


workflow dashboard {
    
    take:
    spatial
    attributes
    intensities
    cells_geo_json
    image
    pixel_size

    main:

    // Cluster the cells
    leiden(intensities)

    // Create anndata object
    anndata(
        spatial,
        attributes,
        leiden.out.clusters,
        leiden.out.scaled_intensities
    )

    // Create spatial data object
    spatialdata(
        anndata.out,
        cells_geo_json,
        image,
        pixel_size
    )

    // Configure the displays using Vitessce 
    configure_vitessce(
        spatialdata.out.kwargs
    )
}