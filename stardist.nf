#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { stardist } from './modules/stardist.nf'
include { dashboard } from './modules/dashboard.nf'

workflow {

    // Check all required parameters
    if("${params.output_folder}" == "false"){
        error "Parameter 'output_folder' must be specified"
    }
    if("${params.input_tiff}" == "false"){
        error "Parameter 'input_tiff' must be specified"
    }

    log.info"""
Inputs / Outputs:
    input_tiff:          ${params.input_tiff}
    output_folder:       ${params.output_folder}

Cell Segmentation - StarDist:
    model:               ${params.model}
    channels:            ${params.channels}
    cellExpansion:       ${params.cellExpansion}
    cellConstrainScale:  ${params.cellConstrainScale}
    container:           ${params.container_stardist}

Dashboard:
    build_dashboard:     ${params.build_dashboard}
    """
    if ("${params.build_dashboard}" == "true") {
    log.info"""
    cluster_by:          ${params.cluster_by}
    cluster_method:      ${params.cluster_method}
    cluster_resolution:  ${params.cluster_resolution}
    cluster_n_neighbors: ${params.cluster_n_neighbors}
    scaling:             ${params.scaling}
    clip_lower:          ${params.clip_lower}
    clip_upper:          ${params.clip_upper}
    """
    }

    // Set up the input file
    input_tiff = file(
        params.input_tiff,
        checkIfExists: true
    )

    // Run StarDist
    stardist(input_tiff)
    cells = stardist.out

    // If the user wants to build the dashboard
    if(params.build_dashboard){

        // Build the dashboard
        dashboard(
            cells.spatial,
            cells.attributes,
            cells.intensities,
            cells.cells_geo_json,
            input_tiff,
            cells.pixel_size
        )

    }

}