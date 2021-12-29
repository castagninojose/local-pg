## Setup and populate local postgreSQL from pandas df

#### Create directory
```bash
cd
mkdir local-dbs
```

#### Pull postgres image and run a docker container with it
```bash
docker pull postgres
docker run -d --name dev-postgres -e POSTGRES_PASSWORD=<your_pwd> -v ${HOME}/local-dbs/:/var/lib/postgresql/data -p 5432:5432 postgres
```

After this, you may need to update permissions on this directory. Simply run `sudo chmod +x ${HOME}/local-dbs`.

#### Enter the container where the DB is running and create a database

```bash
docker exec -it <container-id> bash
```
You can find out the id of the container by running `docker ps`

Now you'll be in the command line of that container. There, you can create a DB using
```bash
psql -U postgres
root@05b3a3471f6f:/# psql -U postgres
postgres-# CREATE DATABASE test-db;
postgres-# GRANT ALL PRIVILEGES ON DATABASE test-db TO $POSTGRES_USER;
postgres-# \q
```

#### Installing the loader

Go to this repository's root directory and install using

```bash
poetry install
```

Once the installation is complete, you'll need to create the table you want your data to be in.
For this, you'll need to declare a couple of things. First, the credentials and connection info
are at `.env` and `cfg.py` respectively. 

:warning: The .env file contains credentials and sensitive information so this is never pushed remotely. See `sample_dot_env` file to get an idea of the things you need to define.

You'll need to find the address of the host, which can be found by running `docker inspect <id> -f "{{json .NetworkSettings.Networks }}"`

Second, you'll have to declare both your table's name and the schema (columns you want it to have). 
You can do this in `/alembic/schema/db_models.py`. Once you make sure everything is set, go to `local-pg/localpg` and run

```bash
poetry run python /alembic/schema/db_models.py
```

This will create the tables declared. Finally, you can populate your DB by going to `localpg/` and running

```bash
poetry run python main.py
```
Check out `main.py` file to make it fit your needs. In there you'll have to write a function that prepares the dataframe you want to insert.

