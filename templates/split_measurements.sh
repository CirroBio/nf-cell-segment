#!/bin/bash
set -euo pipefail

python3 split_measurements.py ${measurements_csv}
