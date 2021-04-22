#!/bin/sh

command=$1
version=$2  # downgrade only

export PYTHONPATH="app:${PYTHONPATH}"
export STAGE=local
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_DATABASE=zappa-flaskrestx
export DB_USER_NAME=root
export DB_PASSWORD=root

(cd `dirname $0`; cd ../)

python ./data_model/migration/manage.py $command $version
