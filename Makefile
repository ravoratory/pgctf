SHELL = /bin/sh

.PHONY: loc
loc: build-loc
	docker compose up

.PHONY: build-loc
build-loc:
	docker compose build

.PHONY: exec
exec:
	docker compose exec web bash

.PHONY: down
down:
	docker compose down

.PHONY: cleanup
clean:
	-docker $(RM) `docker ps -aq`
	docker system prune -af

.PHONY: createsuperuser
cs:
	docker compose exec web \
	python manage.py createsuperuser --noinput

.PHONY: db
db:
	docker compose exec db \
	psql -h 127.0.0.1 -p 5432 -U pg -W postgres
