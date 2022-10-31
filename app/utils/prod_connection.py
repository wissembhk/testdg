from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

sql_database_url = os.getenv("DB_PROD_URL")
engine = create_engine(sql_database_url)
sessionLocalProd = sessionmaker(autocommit=False, bind=engine)
