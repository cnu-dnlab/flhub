#!/bin/bash

python3 -m grpc_tools.protoc -I./ --python_out . --grpc_python_out . flhub.proto
python3 main_database_init.py --reset
