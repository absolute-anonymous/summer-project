from models.database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class University(Base):
    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    salary = Column(Integer)
    average_ege = Column(Float)
    percent_remaining_students = Column(Float)
