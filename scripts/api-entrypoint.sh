#!/bin/bash

set -x

source ~/.bashrc >/dev/null

gunicorn src.iwt_classifier_fastapi.inference_fastapi:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker --timeout 120
