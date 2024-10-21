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

workflow stardist {
    take:
    script
    seg_model
    input_tiff
    stardist_jar

    main:

    qupath_stardist(script, seg_model, input_tiff, stardist_jar)


}