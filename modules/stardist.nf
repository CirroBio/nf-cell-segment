process qupath_stardist {
    container "${params.container}"
    publishDir "${params.output_folder}", mode: 'copy', overwrite: true

    input:
        path script
        path seg_model
        path "input.tiff"
        path stardist_jar

    output:
        path "measurements.csv.gz", emit: measurements_csv
        path "cells.geo.json.gz", emit: cells_geo_json
        path "qupath_project/project.qpproj", emit: project
        path "*"

    script:
    template "stardist.sh"
}


process get_pixel_size {
    container "${params.container_python}"

    input:
        path qupath_project

    output:
        val "pixelWidth"

    script:
    template "get_pixel_size.py"
}


process split_measurements {
    container "${params.container_python}"
    publishDir "${params.output_folder}", mode: 'copy', overwrite: true

    input:
        path measurements_csv

    output:
        path "spatial.csv", emit: spatial
        path "attributes.csv", emit: attributes
        path "*.*.csv", emit: intensities

    script:
    template "split_measurements.py"
}

workflow stardist {
    take:
    script
    seg_model
    input_tiff
    stardist_jar

    main:

    qupath_stardist(script, seg_model, input_tiff, stardist_jar)

    split_measurements(qupath_stardist.out.measurements_csv)

    get_pixel_size(qupath_stardist.out.project)

    emit:
    project = qupath_stardist.out.project
    cells_geo_json = qupath_stardist.out.cells_geo_json
    spatial = split_measurements.out.spatial
    attributes = split_measurements.out.attributes
    intensities = split_measurements.out.intensities
    pixel_size = get_pixel_size.out

}