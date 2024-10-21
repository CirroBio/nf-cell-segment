#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { stardist } from './modules/stardist.nf'

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

}