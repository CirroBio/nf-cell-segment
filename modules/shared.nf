process split_measurements {
    container "${params.container_python}"
    publishDir "${params.output_folder}/cell_measurements", mode: 'copy', overwrite: true

    input:
        path measurements_csv

    output:
        path "spatial.csv", emit: spatial
        path "attributes.csv", emit: attributes
        path "*.*.csv", emit: intensities

    script:
    template "split_measurements.sh"
}
