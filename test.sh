#!/usr/bin/env bash

set -e

# Build Frontend
cd streamlit_markdown/frontend || exit
yarn install
yarn run build

cd ../..

streamlit run example.py --server.fileWatcherType none
