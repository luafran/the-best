root_dir=$1
build_number=$2
dist_dir=${root_dir}/dist

commit_id=$(git rev-parse HEAD)
echo $commit_id

sed -i"" 's/1.0.0/'$commit_id'/g' setup.py

python setup.py egg_info --tag-build ".${build_number}" sdist --dist-dir ${dist_dir}
if [ $? -ne 0 ]; then
    echo "Error: failed to generate pip file"
    exit 1
fi

git checkout -- setup.py