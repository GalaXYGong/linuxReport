from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, DateTime, func, Float, ForeignKey
class Base(DeclarativeBase):
    pass


class Hosts(Base):
    __tablename__ = "hosts"
    id = mapped_column(Integer, primary_key=True)
    hostname = mapped_column(String(250), nullable=False)

class Records(Base):
    __tablename__ = "records"
    id = mapped_column(Integer, primary_key=True)
    host_id = mapped_column(Integer, ForeignKey("hosts.id"), nullable=False)
    file_timestamp = mapped_column(DateTime, nullable=False)
    date_added = mapped_column(DateTime, nullable=False, default=func.now())

class Packages(Base):
    __tablename__ = "packages"
    id = mapped_column(Integer, primary_key=True)
    record_id = mapped_column(Integer, ForeignKey("records.id"), nullable=False)
    package_name = mapped_column(String(250), nullable=False)
    version = mapped_column(String(250), nullable=False)