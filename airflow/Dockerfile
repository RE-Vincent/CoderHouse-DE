# First-time build can take upto 10 mins.

FROM apache/airflow:2.9.1

ENV AIRFLOW_HOME=/opt/airflow

USER root

COPY requirements.txt .
COPY config/airflow.cfg /opt/airflow/config/

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID
RUN pip install --no-cache-dir -r requirements.txt