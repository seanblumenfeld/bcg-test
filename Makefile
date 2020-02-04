.PHONY: help
help:
	@echo "Available commands:"
	@echo "\tclean - stop the running containers and remove pycache folders"
	@echo "\tcreate-env-files - Create local env files"
	@echo "\tbuild - build application"
	@echo "\tstart - run program"
	@echo "\tstart - stop program"
	@echo "\ttest - run tests"
	@echo "\tlint - run lint"

.PHONY: clean
clean:
	-find . -type d -name '__pycache__' -exec rm -rf {} ';'

.PHONY: create-env-file
create-env-files:
ifeq ("$(wildcard .env)","")
	@echo "POSTGRES_USER=bcg" > .env
	@echo "POSTGRES_PASSWORD=CHANGEME" >> .env
	@echo "POSTGRES_DB=bcg" >> .env
endif

.PHONY: build
build: create-env-files clean
	docker-compose build

.PHONY: start
start: build
	$(MAKE) stop
	docker-compose up

.PHONY: start-detached
start-detached: build
	$(MAKE) stop
	docker-compose up -d
	@echo "TODO: implement a service readiness check here"
	@echo "sleeping for 10 seconds..."
	@sleep 10

.PHONY: stop
stop:
	docker-compose down

.PHONY: test
test: build
	docker-compose run web bash -c "python manage.py test --noinput"

.PHONY: lint
lint: build
	docker-compose run web bash -c "flake8 ."

.PHONY: example-post-to-payments-api
example-post-to-payments-api:
	@curl \
		--request POST \
		--header "Content-Type: application/json" \
		--header "X-REQUEST-ID: user-1234" \
		--data '{"amount": "123.45", "token": "some-card-token"}' \
		http://localhost:8000/payments/charge
	@echo ""

