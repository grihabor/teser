docker cp {identity_file}:/project/tests/results.csv {results_path}

docker container rm {identity_file}
docker rmi img:{identity_file}
