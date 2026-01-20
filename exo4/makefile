COMPOSE = docker compose -f docker-compose.yaml

all:
	$(COMPOSE) up --build

clean:
	$(COMPOSE) down

purge_bdd:
	$(COMPOSE) down
	docker volume rm -f exo4_pg_data exo4_pgadmin_data || true

purge_all:
	$(COMPOSE) down --rmi all --volumes --remove-orphans
	rm -rf frontend/node_modules || true

re: purge_all all

.PHONY: all clean purge_bdd purge_all re
