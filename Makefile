clean: 
	docker-compose down --remove-orphans

serve:
	docker-compose up --build system_of_beliefs
