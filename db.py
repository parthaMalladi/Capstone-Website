import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# when running locally
# DATABASE_URL = ""
# engine = create_engine(DATABASE_URL)

# when running online
engine = create_engine(os.environ.get("DATABASE_URL"))

# postgres connection
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
db_session = DBSession()