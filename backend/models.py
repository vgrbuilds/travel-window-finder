from sqlalchemy import Column, Integer, String, Date, Float
from database import Base

class RoadClosure(Base):
    __tablename__ = "road_closures"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String, nullable=True)

class TrafficPattern(Base):
    __tablename__ = "traffic_patterns"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    day_of_week = Column(Integer)
    traffic_score = Column(Float)
