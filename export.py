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
EXCEL_REPORT = pathlib.Path(WORKING_DIR/app_config['excel_report']).absolute()
ENGINE = create_engine(f"sqlite:///{db_path}")


def make_session():
    Session = sessionmaker(bind=ENGINE)
    return Session()

# export to excel file with different sheets for each host
def export_to_excel(output_file):
    import pandas as pd
    session = make_session()
    hosts = session.query(Hosts).all()
    with pd.ExcelWriter(output_file) as writer:
        for host in hosts:
            records = session.query(Records).filter_by(host_id=host.id).all()
            data = []
            for record in records:
                packages = session.query(Packages).filter_by(record_id=record.id).all()
                for pkg in packages:
                    data.append({
                        'hostname': host.hostname,
                        'timestamp': record.file_timestamp,
                        'package_name': pkg.package_name,
                        'version': pkg.version
                    })
            
            df = pd.DataFrame(data)
            # sort by timestamp and package name. Newest timestamp first, and then by package name alphabetically
            df = df.sort_values(by=['timestamp', 'package_name'], ascending=[False, True])
            df.to_excel(writer, sheet_name=host.hostname, index=False)
    print(f"exported report to {output_file}")


if __name__ == "__main__":
    output_file = EXCEL_REPORT
    export_to_excel(output_file)