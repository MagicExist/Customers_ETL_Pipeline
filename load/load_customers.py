import pandas as pd
from sqlalchemy import text




def load_customers(df:pd.DataFrame,engine):
    # Append the cleaned customer rows into the curated destination table.
    df.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False
    )
