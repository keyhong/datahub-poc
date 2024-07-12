FROM apache/airflow:2.8.4

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && gcc --version

RUN chmod 777 /usr/bin/gcc

RUN gcc --version

USER airflow

RUN pip install --upgrade pip \
    && pip install --no-cache-dir \
        acryl-datahub-airflow-plugin[plugin-v2]
        # acryl-datahub-airflow-plugin[plugin-v2]==0.12.1.5 \
        # acryl-datahub==0.12.1.5 \
        # acryl-datahub[mariadb]==0.12.1.5 \
        # apache-airflow-providers-dbt-cloud \
        # openlineage-airflow


# RUN pip install --no-cache-dir acryl-datahub[mariadb]