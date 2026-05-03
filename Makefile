.PHONY: up down clean ingest logs restart

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	docker-compose down -v --rmi local

nuke:
	docker-compose down -v --rmi all

ingest:
	docker-compose run --rm app python ingestion/ingest.py

logs:
	docker-compose logs -f

build:
	docker-compose build app

restart:
	docker-compose restart app