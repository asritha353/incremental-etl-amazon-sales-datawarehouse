# etl/extract.py
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_PATH

def extract_amazon_sales():
    filepath = os.path.join(DATA_PATH, r"C:\Users\asrit\Downloads\amazon_dw_project\data\raw\Amazon Sale Report.csv")
    df = pd.read_csv(filepath, low_memory=False)
    print(f'Extracted {len(df)} rows from Amazon Sale Report')
    return df

def extract_sale_report():
    filepath = os.path.join(DATA_PATH, r"C:\Users\asrit\Downloads\amazon_dw_project\data\raw\Sale Report.csv")
    df = pd.read_csv(filepath)
    print(f'Extracted {len(df)} rows from Sale Report')
    return df

if __name__ == '__main__':
    df = extract_amazon_sales()
    print(df.head())
