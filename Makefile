all: deps up test docs

deps:
	@git submodule update --init

up:
	@vagrant up --no-provision
	@vagrant provision 
	@tox -e db_up
	
test:
	@tox

docs:
	@tox -e docs

.PNONY: all deps up test docs
