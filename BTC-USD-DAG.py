from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import os
import pandas as pd
import yfinance as yf
import psycopg2
import psycopg2.extras
import csv


def insert_some_data():
    bitcoin = yf.Ticker('BTC-USD')
    btc_historical = bitcoin.history(period ='1d', interval ='1m')
    btc_historical.reset_index(inplace=True)
    hook = PostgresHook(postgres_conn_id='turnipdo')
    conn = hook.get_conn()
    cursor = conn.cursor()
    df_BTC = btc_historical
    sql = """INSERT INTO BTC_1m_data(timestamp, Open, High, Low, Close, Volume, Dividends, Stock_Splits) 
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
             ON CONFLICT (timestamp) DO NOTHING"""
    cursor.executemany(sql, df_BTC.values.tolist())
    conn.commit()
    cursor.close()
    conn.close()

with DAG(
    dag_id='BTC_DAG_v3',
    start_date=datetime(2024,1,1),
    schedule=timedelta(minutes=1),
    catchup=False
):
    
    create_table_BTC = SQLExecuteQueryOperator(
    task_id='create_table_BTC',
    conn_id='turnipdo',
    sql="""
            CREATE TABLE IF NOT EXISTS BTC_1m_data(
                timestamp TIMESTAMPTZ PRIMARY KEY,
                Open float,
                High float,
                Low float,
                Close float,
                Volume numeric,
                Dividends float,
                Stock_Splits float
            );
        """
    )

    insert_data_BTC = PythonOperator(
        task_id='insert_data_BTC',
        python_callable=insert_some_data
    )

    create_table_BTC >> insert_data_BTC



    











