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
	python3 -m generator.generator the-kingdom-of-tharg.html 16275216

generate-skylon-tower:
	rm -rf skylon-tower/
	python3 -m generator.generator skylon-tower.html 18655331 short

generate-the-rockets-beneath-us:
	rm -rf the-rockets-beneath-us/
	python3 -m generator.generator the-rockets-beneath-us.html 16281153 short

generate-the-penthouse:
	rm -rf the-penthouse
	python3 -m generator.generator the-penthouse.html 19329824 short

generate-all: generate-the-penthouse generate-the-rockets-beneath-us generate-skylon-tower generate-the-kingdom-of-tharg

test:
	python3 -m generator.tests.parsing

watch-test:
	find . | grep -v .git --include '*.py' | entr -c make test
