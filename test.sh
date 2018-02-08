#!/bin/bash
python timemachine/manage.py test

echo "Linting..."
flake8 timemachine/**/*.py

