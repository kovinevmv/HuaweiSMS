#!/bin/bash

directory_path=$HOME/Desktop/git/HuaweiSMS
python_file=$directory_path/src/main.py

export PYTHONPATH=${directory_path}
python3 $python_file -s