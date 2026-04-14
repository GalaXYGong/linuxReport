import csv, pathlib, os, yaml
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Hosts, Records, Packages

# configurations
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
WORKING_DIR = pathlib.Path(app_config['working_dir'])
DATABASE=app_config['database']
db_path = (WORKING_DIR / DATABASE).absolute()
REPORT_DIR = pathlib.Path(WORKING_DIR/app_config['report_dir']).absolute()

ENGINE = create_engine(f"sqlite:///{db_path}")


def make_session():
    Session = sessionmaker(bind=ENGINE)
    return Session()

def collect_one_report(file_path):
    session = make_session()
    report_file_csv = pathlib.Path(file_path)
    parts = report_file_csv.stem.split("_")
    host_name = parts[0]
    report_time_str = parts[1] + "_" + parts[2]
    dt_obj = datetime.strptime(report_time_str, "%Y%m%d_%H%M%S")
    try:
        host = session.query(Hosts).filter_by(hostname=host_name).first()
        # if host not exist, create a new one
        if not host:
            host = Hosts(hostname=host_name)
            session.add(host)
            session.flush()
        # check if the same report has been imported before, if yes, skip it
        existing_record = session.query(Records).filter_by(host_id=host.id, file_timestamp=dt_obj).first()
        if existing_record:
            print(f"report from {host_name} with timestamp {report_time_str} has already been imported, skipping...")
            return
        # create a new record for this report
        print(f"importing records from {host_name}, timestamp: {report_time_str}")
        new_record = Records(
            host_id=host.id,
            file_timestamp=dt_obj 
        )
        session.add(new_record)
        session.flush() 
        # read CSV and create package entries
        with open(report_file_csv, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row: continue # skip empty lines
                p_name = row[0]
                p_version = row[1]
                package_entry = Packages(
                    record_id=new_record.id,
                    package_name=p_name,
                    version=p_version
                )
                session.add(package_entry)

        # commit all changes
        session.commit()
        print(f"succeeded in importing records from {host_name}, timestamp: {report_time_str}")
    except Exception as e:
        session.rollback() # rollback in case of error
        print(f"write failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # iterate through all csv files in the current directory and import them
    for file in os.listdir(REPORT_DIR):
        if file.endswith(".csv"):
            file_path = REPORT_DIR / file
            collect_one_report(file_path)