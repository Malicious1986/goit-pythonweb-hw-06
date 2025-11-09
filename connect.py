import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

default_url = "postgresql://postgres:1234567@localhost:5432/postgres"
url_to_db = os.environ.get("DATABASE_URL", default_url)

engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
