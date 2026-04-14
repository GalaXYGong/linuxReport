import pathlib, yaml
from models import Base, Packages
from sqlalchemy import create_engine

# configurations
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
WORKING_DIR = pathlib.Path(app_config['working_dir'])
DATABASE=app_config['database']
db_path = (WORKING_DIR / DATABASE).absolute()

ENGINE = create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(ENGINE)