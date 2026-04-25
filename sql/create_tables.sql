--1. DATE DIMENSION
CREATE TABLE IF NOT EXISTS dim_date(
date_key INTEGER PRIMARY KEY,
full_date DATE NOT NULL,
day SMALLINT,
day_name VARCHAR(20),
month SMALLINT,
month_name VARCHAR(20),
quarter SMALLINT,
year INTEGER,
is_weekend BOOLEAN 
);

--2. PRODUCT DIMENSION
CREATE TABLE IF NOT EXISTS dim_product(
product_key SERIAL PRIMARY KEY,
sku VARCHAR(50) UNIQUE NOT NULL,
style VARCHAR(50),
category VARCHAR(50),
size VARCHAR(50),
asin VARCHAR(20)
);

--3. LOCATIN DIMENSION
CREATE TABLE IF NOT EXISTS dim_location(
location_key SERIAL PRIMARY KEY ,
city VARCHAR(100),
state VARCHAR(100),
postal_code VARCHAR(20),
country VARCHAR(10)
);

--4. ORDER STATUS
CREATE TABLE IF NOT EXISTS dim_order_status(
status_key SERIAL PRIMARY KEY,
status_name VARCHAR(100) UNIQUE,
status_category VARCHAR(50)
);

--5. fulfillment DIMENSION
CREATE TABLE IF NOT EXISTS dim_fulfillment(
fulfillment_key SERIAL PRIMARY KEY,
fulfillment_type VARCHAR(50),
service_level VARCHAR(50),
fulfilled_by VARCHAR(50)
);

--6. FACT TABLE
CREATE TABLE IF NOT EXISTS fact_sales(
sales_key SERIAL PRIMARY KEY,
order_id VARCHAR(30),
date_key INTEGER REFERENCES dim_date(date_key),
product_key INTEGER REFERENCES dim_product(product_key),
location_key INTEGER REFERENCES dim_location(location_key),
status_key INTEGER REFERENCES dim_order_status(status_key),
fulfillment_key INTEGER REFERENCES dim_fulfillment(fulfillment_key),
quantity INTEGER,
amount_inr DECIMAL(12,2),
is_b2b BOOLEAN,
currency VARCHAR(5),
load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
source_file VARCHAR(100)
);

--7. ETL WATERMARK TABLE (for incremental loading)
CREATE TABLE IF NOT EXISTS etl_watermark(
table_name VARCHAR(100) PRIMARY KEY,
table_loaded_date DATE,
last_run_at TIMESTAMP
);