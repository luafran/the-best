build_number=$2
root_dir=$1
dist_dir=${root_dir}/dist

python setup.py egg_info --tag-build ".${build_number}" sdist --dist-dir ${dist_dir}
if [ $? -ne 0 ]; then
    echo "Error: failed to generate pip file"
    exit 1
fi
