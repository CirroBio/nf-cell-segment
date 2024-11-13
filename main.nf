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
    if("${params.method}" == "false"){
        error "Parameter 'method' must be specified"
    }

    log.info"""
Parameters:

    input_tiff:     ${params.input_tiff}
    output_folder:  ${params.output_folder}
    method:         ${params.method}
    build_dashboard:${params.build_dashboard}
    cluster_by:     ${params.cluster_by}
    cluster_method: ${params.cluster_method}
    cluster_resolution: ${params.cluster_resolution}
    cluster_n_neighbors: ${params.cluster_n_neighbors}
    scaling:        ${params.scaling}
    clip_lower:     ${params.clip_lower}
    clip_upper:     ${params.clip_upper}
    """

    input_tiff = file(
        params.input_tiff,
        checkIfExists: true
    )

    if(params.method == "stardist"){
        stardist(input_tiff)
        intensities = stardist.out.intensities
        spatial = stardist.out.spatial
        attributes = stardist.out.attributes
        cells_geo_json = stardist.out.cells_geo_json
        pixel_size = stardist.out.pixel_size
    }

    if(params.build_dashboard){

        cluster(intensities)

        dashboard(
            spatial,
            attributes,
            cluster.out.clusters,
            cluster.out.scaled_data,
            cells_geo_json,
            input_tiff,
            pixel_size
        )

    }

}