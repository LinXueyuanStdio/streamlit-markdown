#!/usr/bin/env bash

set -e

# Build Frontend
cd streamlit_markdown/frontend || exit
yarn install
yarn run build

# Build Python package
cd ../..
poetry version patch
poetry build

# Publish to PyPi
# poetry publish
