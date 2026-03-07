from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def raw_db_conn():
    # Load credentials for the database that stores the unprocessed source tables.
    load_dotenv()

    raw_db_user = os.getenv("RAW_DB_USER")
    raw_db_password = os.getenv("RAW_DB_PASSWORD")
    raw_db_host = os.getenv("RAW_DB_HOST")
    raw_db_port = os.getenv("RAW_DB_PORT")
    raw_db_name = os.getenv("RAW_DB_NAME")

    engine = create_engine(
        f"postgresql+psycopg2://{raw_db_user}:{raw_db_password}@{raw_db_host}:{raw_db_port}/{raw_db_name}"
    )

    return engine


def db_conn():
    # Load credentials for the curated database used by the load step.
    load_dotenv()

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    return engine
