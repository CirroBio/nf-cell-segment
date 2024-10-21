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
        path "*"

    script:
    template "stardist.sh"
}

process split_measurements {
    container "${params.container_python}"
    publishDir "${params.output_folder}", mode: 'copy', overwrite: true

    input:
        path measurements_csv

    output:
        path "*.csv"

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


}