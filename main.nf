#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { stardist } from './modules/stardist.nf'
include { cluster } from './modules/cluster.nf'
include { dashboard } from './modules/dashboard.nf'
import groovy.json.JsonSlurper

workflow {

    // Check all required parameters
    if("${params.output_folder}" == "false"){
        error "Parameter 'output_folder' must be specified"
    }
    if("${params.input_tiff}" == "false"){
        error "Parameter 'input_tiff' must be specified"
    }
    if("${params.container}" == "false"){
        error "Parameter 'container' must be specified"
    }

    log.info"""
Parameters:

    input_tiff:     ${params.input_tiff}
    model:          ${params.model}
    output_folder:  ${params.output_folder}
    container:      ${params.container}
    args:           ${params.args}
    """

    input_tiff = file(
        params.input_tiff,
        checkIfExists: true
    )

    seg_model = file(params.model, checkIfExists: true)

    script = file(
        "$projectDir/assets/StarDist_cell_segmentation.groovy",
        checkIfExists: true
    )

    stardist_jar = file(
        "$projectDir/assets/qupath-extension-stardist-0.5.0.jar",
        checkIfExists: true
    )

    stardist(
        script,
        seg_model,
        input_tiff,
        stardist_jar
    )

    if(params.build_dashboard){

        cluster(stardist.out.measurements)

        // Get the pixel size by parsing the qupath metadata
        parse_qupath_project(stardist.out.project)
        parse_qupath_project
            .out
            .apply {
                def jsonSlurper = new JsonSlurper()

            }

        dashboard(
            stardist.out.spatial,
            stardist.out.attributes,
            cluster.out.clusters,
            cluster.out.scaled_data,
            stardist.out.cells_geo_json,
            input_tiff,
            stardist.out.pixel_size
        )

    }

}