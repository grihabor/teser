pwd
eval `ssh-agent`
ssh-add {identity_file_path}

SERVER_KEY=$(ssh-keyscan -t rsa {git.host})
mkdir -p ~/.ssh/
if ! grep -Fxq "$SERVER_KEY" ~/.ssh/known_hosts; then echo $SERVER_KEY >> ~/.ssh/known_hosts; fi

git clone {git.user}@{git.host}:{git.path} user_repo
rm -rf user_repo
