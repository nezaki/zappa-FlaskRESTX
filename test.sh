#!/bin/bash

export PYTHONPATH="app:${PYTHONPATH}"
export STAGE=test
export LOG_LEVEL=DEBUG

(cd `dirname $0`; cd ../)

#pytest
pytest -v --cov=app -s
