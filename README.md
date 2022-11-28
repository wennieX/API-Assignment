## API-Assignment
1. Setup PostgreSQL Using the Public Image
Creat & start container
sudo docker run -it \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=db \
		-e POSTGRES_USER=admin \
    -v /Users/wen/Documents/dockerdata/postgresql/data:/var/lib/postgresql/data \
    --name postgres-server \
    postgres:latest
