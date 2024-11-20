#!/bin/bash

set -euo pipefail

echo "Input file:"
ls -lahtr inputs/*

# If the file extension is .qptiff, make a symlink to .tiff
cd inputs
for file in *.qptiff; do
    if [[ -f "\$file" ]]; then
        echo "Creating symlink for \$file with .tiff extension"
        ln -s "\$file" "\${file%.qptiff}.tiff"
    fi
done
cd ..

echo "Cellpose container: ${params.container_cellpose}"

echo "Parameters:"

echo "Pretrained model: ${params.pretrained_model}"
echo "Channel axis: ${params.channel_axis}"
echo "Segment channel: ${params.segment_channel}"
echo "Diameter: ${params.diameter}"
echo "Flow threshold: ${params.flow_threshold}"
echo "Cellprob threshold: ${params.cellprob_threshold}"

# Set up optional boolean flags
if [[ "${params.no_resample}" == "true" ]]; then
    echo "No resample: enabled"
    no_resample="--no_resample"
else
    echo "No resample: disabled"
    no_resample=""
fi

if [[ "${params.exclude_on_edges}" == "true" ]]; then
    echo "Exclude on edges: enabled"
    exclude_on_edges="--exclude_on_edges"
else
    echo "Exclude on edges: disabled"
    exclude_on_edges=""
fi

if [[ "${params.z_axis}" != "false" ]]; then
    echo "Z axis: ${params.z_axis}"
    z_axis="--z_axis ${params.z_axis}"
else
    echo "Z axis: disabled"
    z_axis=""
fi

if [[ "${params.nuclear_channel}" != "false" ]]; then
    echo "Nuclear channel: ${params.nuclear_channel}"
    chan2="--chan2 ${params.nuclear_channel}"
else
    echo "Nuclear channel: disabled"
    chan2=""
fi

if [[ "${params.anisotropy}" != "false" ]]; then
    echo "Anisotropy: ${params.anisotropy}"
    anisotropy="--anisotropy ${params.anisotropy}"
else
    echo "Anisotropy: disabled"
    anisotropy=""
fi

echo "Running cellpose"
cellpose \
    --pretrained_model "${params.pretrained_model}" \
    --channel_axis "${params.channel_axis}" \
    --chan "${params.segment_channel}" \
    --diameter "${params.diameter}" \
    --flow_threshold "${params.flow_threshold}" \
    --cellprob_threshold "${params.cellprob_threshold}" \
    \$anisotropy \
    \$chan2 \
    \$z_axis \
    \$exclude_on_edges \
    \$no_resample \
    --save_flows \
    --save_outlines \
    --save_tif \
    --dir inputs/ \
    --savedir . \
    --verbose
echo "Done running cellpose"

ls -lahtr *

# Move the cell outlines into the same directory as everything else
mv inputs/*npy ./
