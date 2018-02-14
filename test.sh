#!/bin/bash

set -e

python timemachine/manage.py test

echo "Linting..."
flake8 timemachine/**/*.py

