COMPOSE = docker compose

all:
	docker compose up --build

clean:
	docker compose down

fclean:
	docker compose down --rmi all --volumes --remove-orphans

re: fclean all

.PHONY: all clean fclean re
