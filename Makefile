watch:
	find . | grep -v .git | entr -c docker-compose up --build --force-recreate -d

build:
	./scripts/build.sh

publish:
	./scripts/publish.sh

deploy:
	./scripts/deploy.sh

generate-the-kingdom-of-tharg:
	rm -rf the-kingdom-of-tharg/
	./generate-site.py the-kingdom-of-tharg.html
