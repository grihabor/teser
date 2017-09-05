pwd
eval `ssh-agent`
ssh-add {identity_file_path}
ssh -o StrictHostKeyChecking=no {git.user}@{git.host} ls
git clone {git.user}@{git.host}:{git.path}
cd {repository_name}
docker build . -t img:{identity_file}
docker run img:{identity_file}
rm -rf {repository_name}
