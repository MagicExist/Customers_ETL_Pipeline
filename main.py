import pandas as pd
from config.db import raw_db_conn,db_conn
from extract.extract_customers import extract_customers
from transform.transform_customers import transform_customers
from load.load_customers import load_customers


def main():
    # Read the unvalidated source data from the raw database.
    engine = raw_db_conn()
    df = extract_customers(engine)

    # Normalize and clean the extracted rows before loading them downstream.
    df = transform_customers(df)

    # Write the cleaned dataset into the target database.
    engine = db_conn()
    load_customers(df,engine)



if __name__ == "__main__":
    main()
