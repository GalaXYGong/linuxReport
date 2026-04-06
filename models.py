from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, DateTime, func, Float
class Base(DeclarativeBase):
    pass
class Packages(Base):
    __tablename__ = "packages"
    id = mapped_column(Integer, primary_key=True)
    package_name = mapped_column(String(250), nullable=False)
    version = mapped_column(String(250), nullable=False)
    date_created = mapped_column(DateTime, nullable=False, default=func.now())