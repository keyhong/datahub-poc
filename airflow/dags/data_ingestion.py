"""
This is doc md description.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
import pendulum

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.operators.docker_operator import DockerOperator


from config.dag import build_default_args

dag_args = build_default_args()


# def ingest_from_mysql(datahub_conn):
#     from datahub.ingestion.run.pipeline import Pipeline

#     pipeline = Pipeline.create(
#         # This configuration is analogous to a recipe configuration.
#         {
#             "source": {
#                 "type": "mariadb",
#                 "config": {
#                     # If you want to use Airflow connections, take a look at the snowflake_sample_dag.py example.
#                     "username": "root",
#                     "password": "root",
#                     "database": "test_schema",
#                     "host_port": "airflow-mysql:3306",
#                     "profiling": {
#                         "enabled": True,
#                         "profile_table_level_only": False
#                     },
#                 },
#             },
#             "sink": {
#                 "type": "datahub-rest",
#                 "config": {
#                     "server": datahub_conn.host,
#                     "token": datahub_conn.password
#                 },
#             },
#         }
#     )
#     pipeline.run()
#     pipeline.pretty_print_summary()
#     pipeline.raise_from_status()


@dag(
    dag_id=Path(__file__).stem,
    description=__doc__[0 : __doc__.find(".")],
    doc_md=__doc__,
    default_args=dag_args,
    start_date=pendulum.datetime(2024, 5, 6, tz="Asia/Seoul"),
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["datahub_meta_ingestion"],
)
def generate_dag() -> None:

    # t = docker_operator = DockerOperator(
    #    task_id='ingest_from_mariadb_docker_task',
    #    image='python:slim',
    #    entrypoint="/keytab/kerberos_init.sh",
    #    command="hadoop fs -ls",
    #    environment={"USER_NAME": "gildong@MYHOME.COM", "KEYTAB_PATH": "/keytab/gildong.keytab"},
    #    mounts=[Mount(source='/ext/keytab', target='/keytab', type='bind')],
    #    api_version='auto',
    #    auto_remove=True,
    #    docker_url="unix://var/run/docker.sock",
    #    network_mode="bridge"
    # )


    @task()
    def ingest_from_mariadb(datahub_conn):
        """ingest from mariadb """
        
        from datahub.ingestion.run.pipeline import Pipeline

        # https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/src/datahub/ingestion/run/pipeline_config.py
        # class PipelineConfig(ConfigModel):
        #     source: SourceConfig
        #     sink: Optional[DynamicTypedConfig] = None
        #     transformers: Optional[List[DynamicTypedConfig]] = None
        #     flags: FlagsConfig = Field(default=FlagsConfig(), hidden_from_docs=True)
        #     reporting: List[ReporterConfig] = []
        #     run_id: str = DEFAULT_RUN_ID
        #     datahub_api: Optional[DatahubClientConfig] = None
        #     pipeline_name: Optional[str] = None
        #     failure_log: FailureLoggingConfig = FailureLoggingConfig()


        pipeline = Pipeline.create(
            # This configuration is analogous to a recipe configuration.
            {
                "source": {
                    "type": "mariadb",
                    "config": {
                        # If you want to use Airflow connections, take a look at the snowflake_sample_dag.py example.
                        "username": "root",
                        "password": "root",
                        "database": "test_schema",
                        "host_port": "airflow-mysql:3306",
                        "profiling": {
                            "enabled": True,
                            "profile_table_level_only": False
                        },
                    },
                },
                "sink": {
                    "type": "datahub-rest",
                    "config": {
                        "server": datahub_conn.host,
                        "token": datahub_conn.password
                    },
                },
            }
        )
        pipeline.run()
        pipeline.pretty_print_summary()
        pipeline.raise_from_status()

    # This example pulls credentials from Airflow's connection store.
    # For this to work, you must have previously configured these connections in Airflow.
    # See the Airflow docs for details: https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html


    # from datahub.configuration.config_loader import load_config_file

    # def datahub_recipe(datahub_gms_server):
    #     # Note that this will also resolve environment variables in the recipe.
    #     config = load_config_file("path/to/recipe.yml")

    #     pipeline = Pipeline.create(
    #         # This configuration is analogous to a recipe configuration.
    #         {
    #             "source": {
    #                 "type": "mysql",
    #                 "config": {
    #                     # If you want to use Airflow connections, take a look at the snowflake_sample_dag.py example.
    #                     "username": "root",
    #                     "password": "root",
    #                     "database": "test_schema",
    #                     "host_port": "airflow-mysql:3306",
    #                     "profiling": {"enabled": True},
    #                 },
    #             },
    #             "sink": {
    #                 "type": "datahub-rest",
    #                 "config": {"server": datahub_gms_server},
    #             },
    #         }
    #     )
    #     pipeline.run()


    datahub_conn = BaseHook.get_connection("datahub_rest_default")
    
    ingest_from_mariadb(datahub_conn)


dag_object = generate_dag()

if __name__ == "__main__":
    dag_object.test()
