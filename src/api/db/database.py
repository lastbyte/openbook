from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace these values with your PostgreSQL database information
db_user = 'postgres'
db_password = 'password'
db_host = '0.0.0.0'  # Usually 'localhost' or an IP address
db_port = '5432'  # Default PostgreSQL port
db_name = 'library'

# Create a PostgreSQL connection string
db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
# db_url = "sqlite:///:memory:"


# Create an SQLAlchemy engine to connect to the database
engine = create_engine(db_url)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()

def initialize_sql(engine=engine):
    SessionLocal.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)