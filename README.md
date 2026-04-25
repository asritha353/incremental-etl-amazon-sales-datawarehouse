# Incremental ETL Amazon Sales Data Warehouse

## Architecture
- Source: Amazon Kaggle E-Commerce Dataset (128,000+ rows)
- ETL Tool: Python (Pandas, SQLAlchemy)
- Database: PostgreSQL
- Schema Model: Star Schema (1 Fact Table, 5 Dimension Tables)
- Loading Strategy: Incremental ETL using Watermark Table

## Schema Design

fact_sales →  
- dim_date  
- dim_product  
- dim_location  
- dim_order_status  
- dim_fulfillment

## Key Features
- Incremental data loading (only new records processed)
- Data cleaning, null handling, and standardization
- Surrogate key generation for dimensions
- KPI and business analytics SQL queries
- Modular ETL pipeline (Extract, Transform, Load)

## Technologies Used
- Python 3.10
- PostgreSQL
- Pandas
- SQLAlchemy
- pgAdmin
- GitHub

## How to Run

1. Install dependencies:

pip install -r requirements.txt

2. Configure DB credentials in `config.py`

3. Run pipeline:

python main.py