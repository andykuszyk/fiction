watch:
	find . | grep -v .git | entr -c docker-compose up --build --force-recreate -d

build:
	./scripts/build.sh

publish:
	./scripts/publish.sh

deploy:
	./scripts/deploy.sh
