from models import Base, Packages
from sqlalchemy import create_engine
ENGINE = create_engine("sqlite:///version_database.db")
Base.metadata.create_all(ENGINE)