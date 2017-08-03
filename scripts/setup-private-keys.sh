#!/bin/bash

FILES="master-private_key
worker-private_key"

for f in $FILES
do
    echo "Processing $f"
    cp /vagrant/$f ~
    chmod 600 ~/$f
done

storm_add() {
    OUT="$(storm search $1)"
    if [[ $OUT == "no results found." ]]
    then
        storm add --id_file ~/$1-private_key $1 ubuntu@airflow-$1
    fi
}

storm_add "master"
storm_add "worker"
