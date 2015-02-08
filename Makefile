all: deps up test docs

deps:
	@git submodule update --init

up:
	@vagrant up --no-provision
	@vagrant provision 
	@alembic upgrade head
	
test:
	@tox

docs:
	@tox -e docs

.PNONY: all deps up test docs
