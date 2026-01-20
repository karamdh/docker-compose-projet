COMPOSE = docker compose

all:
	docker compose up --build

clean:
	docker compose down

fclean:
	docker compose down --rmi all --volumes --remove-orphans

purge:
	docker compose down
	rm -rf ./data/*
	docker compose up --build

re: fclean all

.PHONY: all clean fclean purge re
