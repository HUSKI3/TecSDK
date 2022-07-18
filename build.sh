
#!/bin/bash

build_dir="."

while getopts b:a: flag
do
    case "${flag}" in
        u) build_dir=${OPTARG};;
        a) artifacts=${OPTARG};;
    esac
done

hashgen(){
    python3 lib/hashgen.py > artifacts/.hash
}

docker_build(){
    docker build -t tli-portable $build_dir
}

hashgen
docker_build