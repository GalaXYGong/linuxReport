import csv, pathlib, os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Hosts, Records, Packages
ENGINE = create_engine("sqlite:///version_database.db")

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


file_path= "./wujie_20260412_225222.csv"
collect_one_report(file_path)

# iterate through all csv files in the current directory and import them
# one file can only be imported once, if the same file is imported again, it will be skipped