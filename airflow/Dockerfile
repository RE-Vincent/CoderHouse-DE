# First-time build can take upto 10 mins.

FROM apache/airflow:2.9.1-python3.10

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install vim -qqq
# git gcc g++ -qqq

USER airflow
COPY requirements.txt .
COPY config/airflow.cfg /opt/airflow/config/
RUN pip install --no-cache-dir -r requirements.txt

USER root

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID