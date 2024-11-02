.PHONY: network_clean dbinit init login dbattach up down

up:
	docker compose up -d

down:
	docker compose down


# ネットワーク関連
network_clean:
	docker network prune


# PostgreSQLデータベースコンテナ関連
dbinit:
	sudo chown kuro -R data
	sudo chgrp kuro -R data
	# sudo chmod 775 -R data

init:
	psql -U postgres -f setup.sql -d postgres -h localhost -p 5432

login:
	psql -U postgres -d postgres -h localhost -p 5432

login-test-db:
	psql -U postgres -d test_db -h localhost -p 5432

dbattach:
	docker compose logs -f db

backendattach:
	docker compose logs -f backend