#!python3

import json

meta = json.load(open("${qupath_project}"))
px_size = (
    meta
    ["images"]
    [0]
    ["serverBuilder"]
    ["metadata"]
    ["pixelCalibration"]
    ["pixelWidth"]
    ["value"]
)

with open("pixelWidth", "w") as f:
    f.write(str(px_size))
