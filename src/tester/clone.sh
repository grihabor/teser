#!/bin/sh

eval `ssh-agent`
ssh-add {identity_file}
if [ $? -eq 0 ]; then
    echo "ssh-add: ok"
else
    echo "ssh-add: fail"
    exit 1
fi

ssh -o StrictHostKeyChecking=no {user}@{host} ls

git clone {user}@{host}:{path}
if [ $? -eq 0 ]; then
    echo "git clone: ok"
else
    echo "git clone: fail"
    exit 1
fi

