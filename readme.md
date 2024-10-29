### Solution Challengue Franko Miguel

Thanks for the challengue in advance, I enjoyed doing it :+1: .

The solution is just based on a dockerfile for custom DBT and docker compose for include services Airflow , Postgres and DBT.
I used for docker compose for handle it better and share common docker network(Container communicattion)
For simplify and make confortable the execution I included:
* A makefile for just summarize the steps using it.
* requirements for upgrade version when needed
* Docker volumes for share local to containers
* Install dbt utils, tests and docs

**How to run:**
[!NOTE]
Since I used my local and prefer to give some valuable in short time,
the only thing required to change is the paths, I used /home/franko
Also This approach for the challengue uses DockerOperator( In prod I use Astronomer & dbt in virtual env),
[!IMPORTANT]
for use in your local docker just run it before all:
```
sudo chmod o+rw /var/run/docker.sock
```
Then you can build the dbt image
```
make build
```
Next, just run the 
```
make run
```
Once you ran make run, open you browser and go to: http://localhost:8083/dags/franko_lookup_ingest/
user and password airflow & airflow.

Turn in the dag and the dpt dag will run.

[!TIP]
Just in case need to create another project, use:
```
docker exec -it --user root frankomiguel-challenge_my_dbt /bin/bash
cd projects
dbt init --profiles-dir /usr/app
```

If plan to run quries over the postgres db use:
```
sudo docker compose exec -it  my_wh psql -U franko  -c "select replace(covid_for_date,'date_','') as new_col from dev.silver_unpivot_covid_geo limit 10;" my_db
```

**dbt Challenge**

This challenge is designed to evaluate your skills and expertise in working with dbt (data build tool). Your solution will be reviewed not only for its correctness but also for its readability, maintainability, and overall quality. Please note that any documentation or comments in your code will be taken into consideration during the evaluation process, and good practices applied to your solution will be viewed favorably.

**Challenge Description**

You have been provided with a dataset of transactional data from a third-party provider. The data contains various fields with different data types, including dates, strings, and numbers. Your task is to develop a dbt project that reads this data, transforms it into a normalized state, and loads it into a target data warehouse.

**Requirements**

To complete this challenge, you will need to:

1. Create a Docker instance that holds a PostgreSQL database, which will serve as the target data warehouse.
2. Load the provided transactional data into the PostgreSQL database using a Python script.
3. Create a dbt core project and link it to the PostgreSQL instance you created.
4. Create the necessary dbt models to normalize the raw data and create a data mart.

**Deliverables**

Please provide the following:

* A Dockerfile for creating a PostgreSQL-enabled Docker instance
* A Python script with the process to load data into the PostgreSQL instance
* A dbt project that includes:
  * dbt models for normalizing the raw data
  * dbt models for creating a data mart
  * Any additional configuration files or scripts necessary for the solution to work
