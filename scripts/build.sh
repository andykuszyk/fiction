#!/bin/bash
commit=$(git log -n 1 --oneline | awk '{print $1}')
docker build -t andykuszyk/akuszyk:$commit .
