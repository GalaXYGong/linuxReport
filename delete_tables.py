import pathlib
from models import Base, Packages
from sqlalchemy import create_engine

# configurations
WORKING_DIR = pathlib.Path("./")  # set this to the directory where the CSV files are located
DATABASE="version_database.db"
db_path = (WORKING_DIR / DATABASE).absolute()

ENGINE = create_engine(f"sqlite:///{db_path}")
Base.metadata.drop_all(ENGINE)