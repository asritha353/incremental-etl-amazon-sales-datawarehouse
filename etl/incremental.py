# etl/incremental.py
from sqlalchemy import text
from datetime import date
import pandas as pd
from etl.load import get_engine, load_fact

def get_watermark(table_name):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(
            'SELECT last_loaded_date FROM etl_watermark'
            ' WHERE table_name = :t'
        ), {'t': table_name})
        row = result.fetchone()
        return row[0] if row else None


def update_watermark(table_name, new_date):
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text(
            'INSERT INTO etl_watermark(table_name, last_loaded_date, last_run_at)'
            ' VALUES (:t, :d, NOW())'
            ' ON CONFLICT (table_name) DO UPDATE'
            ' SET last_loaded_date = :d, last_run_at = NOW()'
        ), {'t': table_name, 'd': new_date})
        conn.commit()


def incremental_load_facts(df_clean, dims):
    engine = get_engine()
    watermark = get_watermark('fact_sales')

    if watermark is None:
        print('No watermark found. Loading ALL data for first time.')
        new_data = df_clean
    else:
        print(f'Watermark found: {watermark}. Loading data after this date.')
        new_data = df_clean[df_clean['order_date'].dt.date > watermark]

    print(f'New rows to load: {len(new_data)}')

    if len(new_data) > 0:
        load_fact(new_data, dims, engine)

        max_date = new_data['order_date'].max().date()
        update_watermark('fact_sales', max_date)

        print(f'Watermark updated to: {max_date}')
    else:
        print('No new data to load. Pipeline is up to date.')