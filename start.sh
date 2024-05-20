#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
