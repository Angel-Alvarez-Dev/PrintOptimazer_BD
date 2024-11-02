from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL= "postgresql://print_admin:MR.232004@localhost/dbname"

engine = create_engine("URL")
SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)
Base =declarative_base()
