from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL (replace with your own MySQL credentials)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost/scrumreport"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class that can be used for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the models to inherit from
Base = declarative_base()

def get_db():
    db = SessionLocal()  # Open a new session
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Close the session after the request
