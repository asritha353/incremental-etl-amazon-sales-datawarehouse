# etl/load.py
from sqlalchemy import create_engine, text
from config import DB_CONFIG
import pandas as pd

from urllib.parse import quote_plus

def get_engine():
    password = quote_plus(DB_CONFIG['password'])

    url = (f"postgresql://{DB_CONFIG['user']}:{password}"
           f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

    return create_engine(url)


def load_dimension(df, table_name, engine, if_exists='append'):
    df.to_sql(table_name, engine, if_exists=if_exists,
              index=False, method='multi', chunksize=1000)
    print(f'Loaded {len(df)} rows into {table_name}')


def load_fact(df_main, dims, engine):
    # Join dimension keys onto fact
    df = df_main.copy()

    # Date key
    df['date_key'] = df['order_date'].dt.strftime('%Y%m%d').astype(int)

    # Product key
    df = df.merge(dims['product'][['sku','product_key']],
                  on='sku', how='left')

    # Location key
    df = df.merge(dims['location'][['city','state','postal_code','country','location_key']],
                  on=['city','state','postal_code','country'], how='left')

    # Status key
    df = df.merge(dims['status'][['status_name','status_key']],
                  left_on='status', right_on='status_name', how='left')

    # fulfillment key
    df = df.merge(dims['fulfillment'][['fulfillment_type','service_level',
                                       'fulfilled_by','fulfillment_key']],
                  on=['fulfillment_type','service_level','fulfilled_by'], how='left')

    # Select only fact columns
    fact_cols = ['order_id','date_key','product_key','location_key',
                 'status_key','fulfillment_key','quantity','amount_inr',
                 'is_b2b','currency']
    fact_df = df[fact_cols].copy()
    fact_df['source_file'] = 'Amazon Sale Report.csv'

    fact_df.to_sql('fact_sales', engine, if_exists='append',
                   index=False, method='multi', chunksize=500)
    print(f'Loaded {len(fact_df)} rows into fact_sales')

