import pandas as pd
from sqlalchemy import text

def extract_customers(engine):
    # Pull all raw customer records into a DataFrame for in-memory cleaning.
    query = text("""
        SELECT
            *
        FROM customers
                 
    """)

    df = pd.read_sql(query,con=engine)
    return df
