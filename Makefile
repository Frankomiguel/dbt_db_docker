# COLORS
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

.PHONY: build run

all: default

default: help ## help

build:
	echo "Building dbt image"
	sudo docker build -t my_dbt -f Dockerfile_dbt .

run:
	echo "Running Airflow locally using the CeleryExecutor"
	sudo docker compose -f docker-compose.yml up -d

stop:
	sudo docker compose -f docker-compose.yml stop
