process leiden {
    container "${params.container_python}"
    publishDir "${params.output_folder}/cell_clustering", mode: 'copy', overwrite: true

    input:
    path "*"

    output:
    path "leiden_clusters.csv", emit: clusters
    path "scaled_data.csv", emit: scaled_data
    path "*.pdf", emit: plots

    script:
    template "leiden.py"

}

workflow cluster {
    take:
    measurements

    main:
    leiden(measurements)

    emit:
    clusters = leiden.out.clusters
    scaled_data = leiden.out.scaled_data
}