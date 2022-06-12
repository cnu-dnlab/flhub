#!/bin/bash

if [ "$1" != "yes" ] && [ "$1" != "YES" ];
then
    echo "CAUTION SCRIPT"
    echo "Execute $0 yes"
    exit 0
fi

python3 -m grpc_tools.protoc -I./ --python_out . --grpc_python_out . flhub.proto
python3 main_database_init.py --reset
