pwd
eval `ssh-agent`
ssh-add {identity_file_path}

SERVER_KEY=$(ssh-keyscan -t rsa {git.host})
mkdir -p ~/.ssh/
if ! grep -Fxq "$SERVER_KEY" ~/.ssh/known_hosts; then echo $SERVER_KEY >> ~/.ssh/known_hosts; fi

git clone {git.user}@{git.host}:{git.path} user_repo
git clone {git_template.user}@{git_template.host}:{git_template.path} template_repo

cd user_repo
echo "Commit: $(git rev-parse HEAD)"

rm -rf tests Dockerfile
mv ../template_repo/tests ./tests
mv ../template_repo/Dockerfile ./Dockerfile

docker build . -t img:{identity_file}
docker run --name {identity_file} -v compressor_test_files:/project/test_files img:{identity_file}
docker cp {identity_file}:/project/tests/results.csv {results_path}

docker container rm {identity_file}
docker rmi img:{identity_file}

cd ..
rm -rf template_repo user_repo
