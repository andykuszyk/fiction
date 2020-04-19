watch:
	find . | grep -v .git | entr -c docker-compose up --build --force-recreate -d
