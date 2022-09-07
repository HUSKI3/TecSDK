#!/bin/bash

build_dir="."
version=$(git rev-parse --short HEAD | tr -d '\n')

while getopts b:a: flag
do
    case "${flag}" in
        u) build_dir=${OPTARG};;
        a) artifacts=${OPTARG};;
    esac
done

gen_artifacts(){
    python3 lib/hash_gen.py > artifacts/.hash
    python3 lib/config_gen.py > artifacts/config
}

docker_test_build(){
    head -n -1 Dockerfile > testDockerfile
    DOCKER_BUILDKIT=1 docker build -t tli-portable:test -f testDockerfile $build_dir
}

docker_build(){
    DOCKER_BUILDKIT=1 docker build -t tli-portable $build_dir
}

publish_image(){
    DOCKER_BUILDKIT=1 docker build -t huski3/tli-bundle:indev-${version} $build_dir
    docker push huski3/tli-bundle:indev-${version}
    DOCKER_BUILDKIT=1 docker build -t huski3/tli-bundle:latest $build_dir
    docker push huski3/tli-bundle:latest
}

gen_artifacts
docker_test_build
docker_build
publish_image