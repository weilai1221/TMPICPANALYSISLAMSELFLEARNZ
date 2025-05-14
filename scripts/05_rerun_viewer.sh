#!/bin/bash

export CONDA_ENV_NAME=gsicpslam2

if [ -z "$CONDA_DEFAULT_ENV" ] || [ "$CONDA_DEFAULT_ENV" != "$CONDA_ENV_NAME" ]; then
    echo "Conda environment $CONDA_ENV_NAME is not activated" >&2
    exit 1
else
    echo "Conda environment $CONDA_ENV_NAME activated successfully"
fi

python -W ignore gs_icp_slam.py --rerun_viewer