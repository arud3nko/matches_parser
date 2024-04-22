from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Match(Base):
    __tablename__ = 'Matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)
    league = Column(String, nullable=False)
    team1_name = Column(String, nullable=False)
    team2_name = Column(String, nullable=False)
    match_time = Column(String, nullable=False)
    match_url = Column(String, nullable=False)
    match_score = Column(String)
    team1_goals = Column(String)
    team2_goals = Column(String)
