#!/bin/bash
set -euo pipefail

# Add the stardist.jar to qupath
cp "${stardist_jar}" /usr/local/QuPath/lib/app/
sed -i \
    's/\\[Application\\]/\\[Application\\]\\napp.classpath=\$APPDIR\\/${stardist_jar}/' \
    /usr/local/QuPath/lib/app/QuPath.cfg

# sed -i \
#     's/MaxRAMPercentage=50/MaxRAMPercentage=99/' \
#     /usr/local/QuPath/lib/app/QuPath.cfg

cat /usr/local/QuPath/lib/app/QuPath.cfg

echo Working Directory: | tee qupath.log.txt
echo | tee -a qupath.log.txt
ls -lh * | tee -a qupath.log.txt

echo | tee -a qupath.log.txt
echo Starting: | tee -a qupath.log.txt
echo | tee -a qupath.log.txt

mkdir qupath_project

QuPath script \
    "${script}" \
    --args \$PWD/$seg_model \
    --args \$PWD/measurements.csv \
    --args \$PWD/qupath_project \
    --args \$PWD/input.tiff \
    --args \$PWD/cells.geo.json \
    --args ${params.threshold} \
    --args ${params.channels} \
    --args ${params.cellExpansion} \
    --args ${params.cellConstrainScale} \
    --args ${task.cpus} \
    | tee -a qupath.log.txt

gzip measurements.csv
gzip cells.geo.json
