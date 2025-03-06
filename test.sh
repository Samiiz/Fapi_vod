#!/usr/bin/env bash

set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;`

echo "Starting black"
poetry run black .
echo -e "\nok\n"

echo "Starting ruff"
poetry run ruff check --select I --fix
poetry run ruff check --fix
echo -e "\nok\n"

echo -e "Starting mypy"
poetry run mypy .
echo -e "\nok\n"

echo "Starting pytest with coverage"
poetry run coverage run -m pytest
poetry run coverage report -m
poetry run coverage html
echo -e "\nok\n"

echo "${COLOR_GREEN}ALL tests passed seccessfully!${COLOR_NC}"