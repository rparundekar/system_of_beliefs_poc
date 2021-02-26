clean: 
	docker-compose down --remove-orphans

serve:
	docker-compose up --build system_of_beliefs

serve-local-services:
	docker-compose up --detach --build create-minio-buckets