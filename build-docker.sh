#!/bin/bash

build_number=$1
root_dir=$PWD
dist_dir=${root_dir}/dist

python setup.py egg_info --tag-build ".${build_number}" sdist --dist-dir ${dist_dir}
if [ $? -ne 0 ]; then
    echo "Error: failed to generate pip file"
    exit 1
fi

sudo docker build -t quay.io/luafran/the-best:1.0.0 .

#sudo docker login quay.io
#sudo docker push quay.io/luafran/the-best:1.0.0
