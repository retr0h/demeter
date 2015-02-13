all: deps up migrate test docs

deps:
	@git submodule update --init

up:
	@vagrant up --no-provision
	@vagrant provision 
	
test: migrate
	@tox

docs:
	@tox -e docs

migrate:
	@tox -e db_up

.PNONY: all deps up test docs migrate
