include { split_measurements } from './shared.nf'

process find_cells {
    container "${params.container_stardist}"
    publishDir "${params.output_folder}/stardist", mode: 'copy', overwrite: true

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
        path "pixelWidth"

    script:
    template "get_pixel_size.py"
}

workflow stardist {
    take:
    input_tiff

    main:

    if("${params.container_stardist}" == "false"){
        error "Parameter 'container_stardist' must be specified"
    }

    seg_model = file(params.model, checkIfExists: true)

    script = file(
        "$projectDir/assets/StarDist_cell_segmentation.groovy",
        checkIfExists: true
    )

    stardist_jar = file(
        "$projectDir/assets/qupath-extension-stardist-0.5.0.jar",
        checkIfExists: true
    )

    find_cells(script, seg_model, input_tiff, stardist_jar)

    split_measurements(find_cells.out.measurements_csv)

    get_pixel_size(find_cells.out.project)

    emit:
    project = find_cells.out.project
    cells_geo_json = find_cells.out.cells_geo_json
    spatial = split_measurements.out.spatial
    attributes = split_measurements.out.attributes
    intensities = split_measurements.out.intensities
    pixel_size = get_pixel_size.out

}