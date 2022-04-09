run:
	docker compose up --build -d api_dev

db:
	docker compose up --build -d db

psql:
	docker compose exec db psql -U belay_me

tests:
	docker compose up --build api_tests

stop:
	docker-compose down

shell-tests:
	docker compose exec api_tests /bin/bash

shell-api:
	docker compose exec api_dev /bin/bash
