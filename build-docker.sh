#!/bin/bash

build_number=$1

ci/build_packages.sh $PWD ${build_number}

sudo docker build -t quay.io/luafran/the-best:1.0.${build_number} .

#sudo docker login quay.io
sudo docker push quay.io/luafran/the-best:1.0.${build_number}
