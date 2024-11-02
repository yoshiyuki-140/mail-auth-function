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
	sudo chown 999 -R data
	sudo chgrp 999 -R data
	# sudo chmod 775 -R data

init:
	psql -U psql -f setup.sql -d psql -h localhost -p 5432

login:
	psql -U psql -d psql -h localhost -p 5432

dbattach:
	docker compose logs -f db

backendattach:
	docker compose logs -f backend