# ETL Process PG

Small Python ETL project that extracts customer data from a raw PostgreSQL database, cleans and standardizes it with Pandas, and loads the result into a second PostgreSQL database.

## What This Project Does

The pipeline is built around one table: `customers`.

It follows a classic ETL flow:

1. Extract raw customer rows from a source database.
2. Transform the data by cleaning invalid values and normalizing formats.
3. Load the cleaned rows into a curated destination database.

This project is useful as a simple example of how to:

- connect Python to PostgreSQL with SQLAlchemy
- move data with Pandas DataFrames
- clean inconsistent source data before loading it into a typed table

## Project Structure

```text
ETL_Process_PG/
├── main.py
├── config/
│   └── db.py
├── extract/
│   └── extract_customers.py
├── transform/
│   └── transform_customers.py
├── load/
│   └── load_customers.py
└── sql/
    ├── raw_tables.sql
    └── clean_table.sql
```

## How The Pipeline Works

### 1. Extract

[`extract/extract_customers.py`](extract/extract_customers.py) reads every row from the raw `customers` table into a Pandas DataFrame.

### 2. Transform

[`transform/transform_customers.py`](transform/transform_customers.py) applies the cleaning pipeline. It:

- converts empty strings and `"NaN"` placeholders to null values
- removes rows missing required fields such as `full_name`, `email`, or `birth_date`
- lowercases and trims text fields
- removes duplicate customers based on `full_name`
- invalidates malformed emails
- cleans phone numbers and keeps only 10-digit values
- normalizes country values like `COL` to `colombia`
- parses mixed birth date and timestamp formats
- converts `total_spent` to numeric values
- converts `is_active` into boolean values

### 3. Load

[`load/load_customers.py`](load/load_customers.py) appends the cleaned DataFrame into the destination `customers` table with `DataFrame.to_sql(...)`.

### 4. Orchestration

[`main.py`](main.py) runs the full ETL flow in order:

1. connect to the raw database
2. extract raw rows
3. transform them
4. connect to the target database
5. load the cleaned rows

## Database Setup

The `sql/` folder contains two schema scripts:

- [`sql/raw_tables.sql`](sql/raw_tables.sql): creates the raw source table and inserts messy sample data
- [`sql/clean_table.sql`](sql/clean_table.sql): creates the curated destination table with typed columns and a unique constraint on `email`

Recommended setup:

1. Create a raw PostgreSQL database.
2. Run `sql/raw_tables.sql` in that database.
3. Create a second PostgreSQL database for clean data.
4. Run `sql/clean_table.sql` in the destination database.

## Environment Variables

[`config/db.py`](config/db.py) reads connection settings from a `.env` file.

Required variables:

```env
RAW_DB_USER=your_raw_db_user
RAW_DB_PASSWORD=your_raw_db_password
RAW_DB_HOST=localhost
RAW_DB_PORT=5432
RAW_DB_NAME=raw_database_name

DB_USER=your_target_db_user
DB_PASSWORD=your_target_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clean_database_name
```

## Requirements

This project uses:

- Python
- pandas
- SQLAlchemy
- psycopg2
- python-dotenv

Example installation:

```bash
pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

## How To Run

From the project root:

```bash
python main.py
```

If the database connections are correct, the script will extract the raw customer records, transform them, and append the cleaned results into the destination table.

## Example Use Case

The sample raw data includes common real-world data quality problems:

- duplicated customers
- invalid emails
- inconsistent capitalization
- phone numbers with symbols or country prefixes
- mixed date formats
- boolean values stored as text
- numeric values stored as strings

The ETL process converts that messy input into a more reliable table for analytics or application use.

## Notes

- The load step uses `if_exists="append"`, so each run inserts more rows into the destination table.
- The destination table enforces `UNIQUE` on `email`, so repeated loads can fail if the same cleaned email is inserted more than once.
- The transformation rules are currently specific to the `customers` dataset.
