#!/bin/bash

export AIMRT_PLUGIN_DIR=$(pip show aimrt_py | grep Location | awk '{print $2}')/aimrt_py

source ${AIMRT_PLUGIN_DIR}/share/ros2_plugin_proto/local_setup.bash

python3 benchmark_publisher_app.py --cfg_file_path ./cfg/benchmark_publisher_cfg.yaml
