"""
This is doc md description.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
import pendulum

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonVirtualenvOperator

from config.dag import build_default_args

dag_args = build_default_args()

def ingest_from_mysql(datahub_gms_server):
    from datahub.ingestion.run.pipeline import Pipeline

    pipeline = Pipeline.create(
        # This configuration is analogous to a recipe configuration.
        {
            "source": {
                "type": "mysql",
                "config": {
                    # If you want to use Airflow connections, take a look at the snowflake_sample_dag.py example.
                    "username": "root",
                    "password": "root",
                    "database": "test_schema",
                    "host_port": "airflow-mysql:3306",
                    "profiling": {"enabled": True},
                },
            },
            "sink": {
                "type": "datahub-rest",
                "config": {"server": datahub_gms_server},
            },
        }
    )
    pipeline.run()
    pipeline.pretty_print_summary()
    pipeline.raise_from_status()


@dag(
    dag_id=Path(__file__).stem,
    description=__doc__[0: __doc__.find(".")],
    doc_md=__doc__,
    default_args=dag_args,
    start_date=pendulum.datetime(2024, 5, 6, tz="Asia/Seoul"),
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["datahub_meta_ingestion"],
)
def generate_dag() -> None:

    # @task
    # def ingest_from_mysql():
    #     from datahub.ingestion.run.pipeline import Pipeline

    #     # https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/src/datahub/ingestion/run/pipeline_config.py
    #     # class PipelineConfig(ConfigModel):
    #     #     source: SourceConfig
    #     #     sink: Optional[DynamicTypedConfig] = None
    #     #     transformers: Optional[List[DynamicTypedConfig]] = None
    #     #     flags: FlagsConfig = Field(default=FlagsConfig(), hidden_from_docs=True)
    #     #     reporting: List[ReporterConfig] = []
    #     #     run_id: str = DEFAULT_RUN_ID
    #     #     datahub_api: Optional[DatahubClientConfig] = None
    #     #     pipeline_name: Optional[str] = None
    #     #     failure_log: FailureLoggingConfig = FailureLoggingConfig()

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
    #                 },
    #             },
    #             "sink": {
    #                 "type": "datahub-rest",
    #                 "config": {
    #                     "server": "http://datahub-gms:8080",
    #                     "token": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6Ijc4MDczNDA1LWNkNGYtNGMyNi05YzU2LTIwNDNmNjRlNzhjMCIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3MjI0MTUzMDMsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.r-gDDxQDucLfmSOSvBWq3l3IUlpimwMS0CU2-wHKQMg",
    #                 },
    #             },
    #         }
    #     )
    #     pipeline.run()
    #     pipeline.pretty_print_summary()
    #     pipeline.raise_from_status()

    # This example pulls credentials from Airflow's connection store.
    # For this to work, you must have previously configured these connections in Airflow.
    # See the Airflow docs for details: https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html
    datahub_conn = BaseHook.get_connection("datahub_rest_default")

    # While it is also possible to use the PythonOperator, we recommend using
    # the PythonVirtualenvOperator to ensure that there are no dependency
    # conflicts between DataHub and the rest of your Airflow environment.
    ingest_task = PythonVirtualenvOperator(
        task_id="ingest_task",
        requirements=[
            "acryl-datahub==0.12.1.5",
            "acryl-datahub==0.12.1.5",
            "acryl-datahub[mariadb]==0.12.1.5",
        ], 
        system_site_packages=False,
        python_callable=ingest_from_mysql,
        op_kwargs={
            # "snowflake_credentials": {
            #     "username": snowflake_conn.login,
            #     "password": snowflake_conn.password,
            #     "account_id": snowflake_conn.extra_dejson["account"],
            #     "warehouse": snowflake_conn.extra_dejson.get("warehouse"),
            #     "role": snowflake_conn.extra_dejson.get("role"),
            # },
            "datahub_gms_server": datahub_conn.host,
        },
    )

dag_object = generate_dag()

if __name__ == "__main__":
    dag_object.test()
