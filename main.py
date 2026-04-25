# main.py — Full ETL Pipeline Runner
from etl.extract import extract_amazon_sales
from etl.transform import (clean_amazon_sales, build_dim_date,
    build_dim_product, build_dim_location,
    build_dim_status, build_dim_fulfillment)
from etl.load import get_engine, load_dimension, load_fact
from etl.incremental import incremental_load_facts

def run_pipeline():
    print('='*50)
    print('STARTING ETL PIPELINE')
    print('='*50)

    # STEP 1: EXTRACT
    print('\n--- EXTRACT ---')
    raw_df = extract_amazon_sales()

    # STEP 2: TRANSFORM
    print('\n--- TRANSFORM ---')
    clean_df = clean_amazon_sales(raw_df)
    dim_date = build_dim_date(clean_df)
    dim_product = build_dim_product(clean_df)
    dim_location = build_dim_location(clean_df)
    dim_status = build_dim_status(clean_df)
    dim_fulfillment = build_dim_fulfillment(clean_df)

    # STEP 3: LOAD DIMENSIONS
    print('\n--- LOAD DIMENSIONS ---')
    engine = get_engine()
    load_dimension(dim_date, 'dim_date', engine, if_exists='append')
    load_dimension(dim_product, 'dim_product', engine, if_exists='append')
    load_dimension(dim_location, 'dim_location', engine, if_exists='append')
    load_dimension(dim_status, 'dim_order_status', engine, if_exists='append')
    load_dimension(dim_fulfillment, 'dim_fulfillment', engine, if_exists='append')

    # STEP 4: INCREMENTAL LOAD FACTS
    print('\n--- LOAD FACTS (INCREMENTAL) ---')
    dims = {'product': dim_product, 'location': dim_location,
            'status': dim_status, 'fulfillment': dim_fulfillment}
    incremental_load_facts(clean_df,dims)

    print('\n' + '='*50)
    print('ETL PIPELINE COMPLETED SUCCESSFULLY')
    print('='*50)

if __name__ == '__main__':
    run_pipeline()

