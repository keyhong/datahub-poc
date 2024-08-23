from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago

# 기본 DAG 인수 정의
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

# DAG 정의
dag = DAG(
    "postgres_operator_example",
    default_args=default_args,
    description="A simple DAG using PostgresOperator",
    schedule_interval=None,  # DAG을 자동으로 실행하지 않도록 설정
    start_date=days_ago(1),
    catchup=False,
)

# SQL 쿼리 정의
create_table_sql = """
CREATE TABLE IF NOT EXISTS stg.example_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# PostgresOperator 정의
create_table = PostgresOperator(
    task_id="create_table",
    sql=create_table_sql,
    postgres_conn_id="postgres_conn",  # Airflow Connections에서 정의된 연결 ID
    dag=dag,
)

# DAG의 작업 순서 정의 (여기서는 단일 작업만 있음)
create_table
