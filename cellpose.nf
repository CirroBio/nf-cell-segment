#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { cellpose } from './modules/cellpose.nf'
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

Cell Segmentation - Cellpose:
    model:               ${params.model}
    channel_axis:        ${params.channel_axis}
    z_axis:              ${params.z_axis}
    segment_channel:     ${params.segment_channel}
    nuclear_channel:     ${params.nuclear_channel}
    no_resample:         ${params.no_resample}
    diameter:            ${params.diameter}
    flow_threshold:      ${params.flow_threshold}
    cellprob_threshold:  ${params.cellprob_threshold}
    anisotropy:          ${params.anisotropy}
    exclude_on_edges:    ${params.exclude_on_edges}
    container:           ${params.container_cellpose}

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

    // Run cellpose
    cellpose(input_tiff)
    cells = cellpose.out

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