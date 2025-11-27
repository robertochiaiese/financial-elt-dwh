import logging 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from pathlib import Path
import os
import datetime

database = 'marketdata' #os.getenv("POSTGRES_DB")
usr = 'roberto' #os.getenv("POSTGRES_USER")
psw = 'password' #os.getenv("POSTGRES_PASSWORD")
port = '5000' #os.getenv("POSTGRES_PORT")
host = 'localhost' #os.getenv("POSTGRES_HOST")

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "logging_db.log"



logging.basicConfig(
    format="%(name)s:%(asctime)s:%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
    filename=LOG_FILE,
    filemode='w'
    )

logger = logging.getLogger(__name__)

def connect_to_db(host,database,usr,psw,port):
    logger.info(f"Connecting to the database...")
    try:

        postgres_str = f"postgresql+psycopg2://{usr}:{psw}@{host}:{port}/{database}"
        engine = create_engine(postgres_str)
        logger.info(f"Succesfully connected to the database {database}")
        return engine
    
    except SQLAlchemyError as e:
        logger.error(f"Error during the connection to the database: {e}")
