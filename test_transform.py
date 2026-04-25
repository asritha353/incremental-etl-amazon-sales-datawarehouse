from etl.extract import extract_amazon_sales
from etl.transform import clean_amazon_sales

df = extract_amazon_sales()
clean_df = clean_amazon_sales(df)

print(clean_df.head())
print(clean_df.columns)