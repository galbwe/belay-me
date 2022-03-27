#! /bin/bash

# This script is used to setup the local development environment.

# To run this script you will need python 3.10.4 installed

cd backend && \
    python -m venv venv && \
    source venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    deactivate && \
    cd ..