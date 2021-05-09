SHELL = /bin/sh
COMPOSE_LOCAL := docker-compose.local.yml
compose = docker-compose -f $(COMPOSE_LOCAL)

.PHONY: loc
loc: build-loc
	$(compose) up

.PHONY: build-loc
build-loc:
	$(compose) build

.PHONY: exec
exec:
	$(compose) exec web bash

.PHONY: exec-db
exec-db:
	$(compose) exec db bash

.PHONY: down
down:
	$(compose) down

.PHONY: cleanup
clean:
	-docker $(RM) `docker ps -aq`
	docker system prune -af

user = root
email = root@example.com

.PHONY: cs
cs:
	$(compose) exec web \
	python manage.py createsuperuser --username $(user) --email $(email)

.PHONY: db
db:
	$(compose) exec db \
	psql -h 127.0.0.1 -p 5432 -U pg -W postgres
