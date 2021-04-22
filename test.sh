#!/bin/bash

export PYTHONPATH="app:${PYTHONPATH}"
export STAGE=test

(cd `dirname $0`; cd ../)

pytest
