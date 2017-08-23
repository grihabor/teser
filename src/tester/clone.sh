#!/bin/sh

eval `ssh-agent`
ssh-add {identity_file}
if [ $? -eq 0 ]; then
    echo "ssh-add: ok"
    git clone {user}@{host}:{path}
else
    echo "ssh-add: fail"
fi

