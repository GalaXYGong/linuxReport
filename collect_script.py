import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
ENGINE = create_engine("sqlite:///change-me-to-something-nice.db")

def make_session():
    Session = sessionmaker(bind=ENGINE)
    return Session()

report_file_csv = "./wujie_20260405164424.csv"
# with open(report_file_csv, 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         print(row)

    