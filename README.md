## API-Assignment
Basic personal information register API. Use FastAPI and Docker container
(Postgresql) to implement. It is not deployed to any server by a single
command yet, just basic setups and running successfully.

**1. Database:** setup a postgres database to run on `localhost`
with a user `admin` and password `test`. The port is default 
`5432`, and there should be a database named `db`.


[//]: # (**1. Setup PostgreSQL Using the Public Image**)
Commands:

```
# 1. Creat & start container 
# Replace /data/path/on/host with any folder on you host machine.
sudo docker run -it \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=db \
        -e POSTGRES_USER=admin \
    -v /data/path/on/host:/var/lib/postgresql/data \
    --name postgres-server \
    postgres:latest
    
# 2. Create database
docker exec -it postgres-server sh
psql -d db -U admin -W
```
Initialize it with the schema defined at `database/create.sql`.

**2. Backend:** install python requirements(`requirements.txt`)
and run by:`python main.py`. It will run at `localhost:5000`.



