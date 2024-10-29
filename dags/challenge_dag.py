
"""
NOTE:
    Run this in your local for use docker:
        sudo chmod o+rw /var/run/docker.sock

DAG for approve Loopstudio challengue using DBT, Postgres & Airflow, steps:

    Steps 1:
        - Install dbt utils for use unpivot
    Step 2:
        - Load the Covid csv file using dbt seed (Raw data)
    Step 3:
        - Apply dbt run for transform and clean stage(silver) data
    step4:
        - Test the data using dbt tests for stage models
    step 5:
        - Run the dbt models for target(gold)
    step 6:
        - Execute dbt docs for generate docs
    step 7:
        - Just expose dbt docs in http://localhost:8085 for lineage and context

"""

from __future__ import annotations

import logging
import sys
import pendulum
from airflow.models.dag import DAG
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator


log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable


with DAG(
    dag_id="franko_lookup_ingest",
    schedule="0 8 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
):


    dependencies = DockerOperator(
        task_id='ti_install_dbt_utils',
        image='my_dbt',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        command='sh -c "dbt deps --project-dir /usr/app/projects/franko"',
        mounts=[Mount(source='/home/franko/Documents/repos/Frankomiguel-challenge/dbt_directory',target='/usr/app',type='bind')],
        mount_tmp_dir=False,
        network_mode='container:frankomiguel-challenge_my_dbt'
    )
    create_seed = DockerOperator(
        task_id='ti_load_raw_data',
        image='my_dbt',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        command='sh -c "cd projects && dbt seed --project-dir /usr/app/projects/franko --target dev --profiles-dir /usr/app" --threads 4',
        mounts=[Mount(source='/home/franko/Documents/repos/Frankomiguel-challenge/dbt_directory',target='/usr/app',type='bind')],
        mount_tmp_dir=False,
        network_mode='container:frankomiguel-challenge_my_dbt'
    )

    stage_model = DockerOperator(
        task_id='ti_load_stage_data',
        image='my_dbt',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        command='sh -c "dbt run --select silver --project-dir /usr/app/projects/franko --target dev --profiles-dir /usr/app"',
        mounts=[Mount(source='/home/franko/Documents/repos/Frankomiguel-challenge/dbt_directory',target='/usr/app',type='bind')],
        mount_tmp_dir=False,
        network_mode='container:frankomiguel-challenge_my_dbt'
    )

    test_stage_model = DockerOperator(
        task_id='ti_test_stage_data',
        image='my_dbt',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        command='sh -c "dbt test --select silver --project-dir /usr/app/projects/franko --target dev --profiles-dir /usr/app"',
        mounts=[Mount(source='/home/franko/Documents/repos/Frankomiguel-challenge/dbt_directory',target='/usr/app',type='bind')],
        mount_tmp_dir=False,
        network_mode='container:frankomiguel-challenge_my_dbt'
    )

    target_model = DockerOperator(
        task_id='ti_load_target_data',
        image='my_dbt',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        command='sh -c "dbt run --select golden --project-dir /usr/app/projects/franko --target dev --profiles-dir /usr/app"',
        mounts=[Mount(source='/home/franko/Documents/repos/Frankomiguel-challenge/dbt_directory',target='/usr/app',type='bind')],
        mount_tmp_dir=False,
        network_mode='container:frankomiguel-challenge_my_dbt'
    )

    docs_generate = DockerOperator(
        task_id='ti_docs_generate',
        image='my_dbt',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        command='sh -c "dbt docs generate --no-compile --project-dir /usr/app/projects/franko --target dev --profiles-dir /usr/app"',
        mounts=[Mount(source='/home/franko/Documents/repos/Frankomiguel-challenge/dbt_directory',target='/usr/app',type='bind')],
        mount_tmp_dir=False,
        network_mode='container:frankomiguel-challenge_my_dbt'
    )

    docs_serve = DockerOperator(
        task_id='ti_docs_serve',
        image='my_dbt',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        command='sh -c "dbt docs serve  --port 8085 --project-dir /usr/app/projects/franko --target dev --profiles-dir /usr/app"',
        mounts=[Mount(source='/home/franko/Documents/repos/Frankomiguel-challenge/dbt_directory',target='/usr/app',type='bind')],
        mount_tmp_dir=False,
        network_mode='container:frankomiguel-challenge_my_dbt'
    )
    dependencies >>  create_seed >> stage_model >> test_stage_model >> target_model>>docs_generate >> docs_serve
