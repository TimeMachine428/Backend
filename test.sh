#!/bin/bash

set -e

python timemachine/manage.py test restapi

echo "Linting..."
flake8 timemachine/**/*.py

