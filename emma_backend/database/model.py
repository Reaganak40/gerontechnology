from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


metadata = MetaData()
calculations = Table('Calculations', metadata,
    Column('week_number', Integer, primary_key=True),
    Column('year_number', Integer, primary_key=True),
    Column('participant_id', Integer, ForeignKey('Participants.participant_id'), primary_key=True),
    )

Base = declarative_base()
class Participant(Base):
    # The SQL Table this references
    __tablename__ = "Participants"

    # SQL Columns for Table Participants
    participant_id = Column(Integer, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))

def test_conn():
    results = engine.execute("SELECT * FROM Participants").fetchall()
    for r in results:
        print(r)

if __name__ == "__main__":
    test_conn()
