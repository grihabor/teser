pwd
eval `ssh-agent`
ssh-add {identity_file_path}
ssh -o StrictHostKeyChecking=no {git.user}@{git.host} ls
git clone {git.user}@{git.host}:{git.path}
rm -rf {repository_name}
