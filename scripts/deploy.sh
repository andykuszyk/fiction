#!/bin/bash
commit=$(git log -n 1 --oneline | awk '{print $1}')
echo "About to deploy commit: $commit"
echo "Compose file before transforms:"
cat docker-compose.yml

sed -i "s/build:.*/image: andykuszyk\/akuszyk:$commit/g" docker-compose.yml
sed -i 's/.*port.*//g' docker-compose.yml
sed -i 's/.*80.*//g' docker-compose.yml

echo "Compose file after transforms:"
cat docker-compose.yml

scp -i id_rsa -o "StrictHostKeyChecking no" ./docker-compose.yml $douser@$doip:~/docker-compose.yml
ssh -i id_rsa -o "StrictHostKeyChecking no" $douser@$doip "docker stack deploy -c ~/docker-compose.yml szyk"
