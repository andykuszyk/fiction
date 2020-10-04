#!/bin/bash
commit=$(git log -n 1 --oneline | awk '{print $1}')
git clone https://andykuszyk:$GITHUB_TOKEN@github.com/andykuszyk/do-docker
cd do-docker
make release-service SERVICE=akuszyk TAG=$commit
