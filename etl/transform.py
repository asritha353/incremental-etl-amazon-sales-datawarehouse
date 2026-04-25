# etl/transform.py
import pandas as pd


def clean_amazon_sales(df):
    # Rename raw dataset columns to warehouse-friendly names
    df = df.rename(columns={
        'Order ID': 'order_id',
        'Date': 'order_date',
        'Status': 'status',
        'Fulfilment': 'fulfillment_type',
        'Sales Channel ': 'sales_channel',
        'ship-service-level': 'service_level',
        'Style': 'style',
        'SKU': 'sku',
        'Category': 'category',
        'Size': 'size',
        'ASIN': 'asin',
        'Qty': 'quantity',
        'currency': 'currency',
        'Amount': 'amount_inr',
        'ship-city': 'city',
        'ship-state': 'state',
        'ship-postal-code': 'postal_code',
        'ship-country': 'country',
        'B2B': 'is_b2b',
        'fulfilled-by': 'fulfilled_by'
    })

    # Convert date column
    df['order_date'] = pd.to_datetime(
        df['order_date'],
        format='%m-%d-%y',
        errors='coerce'
    )

    # Handle missing values
    df['amount_inr'] = df['amount_inr'].fillna(0)
    df['quantity'] = df['quantity'].fillna(0).astype(int)
    df['city'] = df['city'].fillna('UNKNOWN').str.title()
    df['state'] = df['state'].fillna('UNKNOWN').str.title()
    df['postal_code'] = df['postal_code'].fillna(0)
    df['country'] = df['country'].fillna('UNKNOWN')
    df['fulfilled_by'] = df['fulfilled_by'].fillna('UNKNOWN')
    df['fulfillment_type'] = df['fulfillment_type'].fillna('UNKNOWN')
    df['service_level'] = df['service_level'].fillna('UNKNOWN')
    df['currency'] = df['currency'].fillna('INR')

    # Status category
    def categorise_status(s):
        s = str(s).lower()

        if 'cancelled' in s:
            return 'Cancelled'
        elif 'delivered' in s:
            return 'Completed'
        elif 'shipped' in s:
            return 'In Transit'
        else:
            return 'Other'

    df['status_category'] = df['status'].apply(categorise_status)

    # Remove bad rows
    df = df.dropna(subset=['order_date', 'order_id'])

    print(f'After cleaning: {len(df)} rows remain')
    return df


def build_dim_date(df):
    dates = df['order_date'].drop_duplicates()

    dim = pd.DataFrame({'full_date': dates})
    dim['date_key'] = dim['full_date'].dt.strftime('%Y%m%d').astype(int)
    dim['day'] = dim['full_date'].dt.day
    dim['day_name'] = dim['full_date'].dt.day_name()
    dim['month'] = dim['full_date'].dt.month
    dim['month_name'] = dim['full_date'].dt.strftime('%B')
    dim['quarter'] = dim['full_date'].dt.quarter
    dim['year'] = dim['full_date'].dt.year
    dim['is_weekend'] = dim['full_date'].dt.dayofweek >= 5

    return dim


def build_dim_product(df):
    cols = ['sku', 'style', 'category', 'size', 'asin']

    dim = df[cols].drop_duplicates(subset=['sku']).reset_index(drop=True)
    dim.insert(0, 'product_key', range(1, len(dim) + 1))

    return dim


def build_dim_location(df):
    cols = ['city', 'state', 'postal_code', 'country']

    dim = df[cols].drop_duplicates().reset_index(drop=True)
    dim.insert(0, 'location_key', range(1, len(dim) + 1))

    return dim


def build_dim_status(df):
    dim = df[['status', 'status_category']].drop_duplicates()
    dim = dim.rename(columns={'status': 'status_name'})
    dim = dim.reset_index(drop=True)
    dim.insert(0, 'status_key', range(1, len(dim) + 1))

    return dim


def build_dim_fulfillment(df):
    cols = ['fulfillment_type', 'service_level', 'fulfilled_by']

    dim = df[cols].drop_duplicates().reset_index(drop=True)
    dim.insert(0, 'fulfillment_key', range(1, len(dim) + 1))

    return dim