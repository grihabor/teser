#!/bin/sh

eval `ssh-agent`
ssh-add {identity_file}
echo {identity_file} | git clone {user}@{host}:{path}
