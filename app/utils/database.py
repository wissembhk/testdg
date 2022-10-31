from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

sql_database_url = os.getenv("DB_URL")
engine = create_engine(sql_database_url)
sessionLocal = sessionmaker(autocommit=False, bind=engine)
base = declarative_base()


def create_db():
    return base.metadata.create_all(bind=engine)
