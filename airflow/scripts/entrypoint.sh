#!/usr/bin/env bash

# set -e

# # Ruta relativa al archivo .env
# ENV_FILE="/opt/airflow/.env"

# # Cargar variables de entorno del archivo .env
# # if [ -f "$ENV_FILE" ]; then
# #     export $(cat "$ENV_FILE" | grep -v '#' | awk '/=/ {print $1}')
# # fi
# if [ -f "$ENV_FILE" ]; then
#     set -o allexport
#     source "$ENV_FILE"
#     set +o allexport
# fi

airflow db upgrade

airflow users create -r Admin -u admin -p admin -e admin@example.com -f admin -l airflow
# "$_AIRFLOW_WWW_USER_USERNAME" -p "$_AIRFLOW_WWW_USER_PASSWORD"

airflow webserver