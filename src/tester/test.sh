pwd
eval `ssh-agent`
ssh-add {identity_file_path}

SERVER_KEY=$(ssh-keyscan -t rsa {git.host})
mkdir -p ~/.ssh/
if ! grep -Fxq "$SERVER_KEY" ~/.ssh/known_hosts; then echo $SERVER_KEY >> ~/.ssh/known_hosts; fi

git clone {git.user}@{git.host}:{git.path}
cd {repository_name}
docker build . -t img:{identity_file}
docker run img:{identity_file}
rm -rf {repository_name}
