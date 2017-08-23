#!/bin/sh

eval `ssh-agent`
ssh-add {identity_file}
if [ $? -eq 0 ]; then
    echo "ssh-add: ok"
    ssh -o StrictHostKeyChecking=no {user}@{host} ls
    git clone {user}@{host}:{path}
else
    echo "ssh-add: fail"
fi

