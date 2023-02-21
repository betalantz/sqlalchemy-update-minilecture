#!/usr/bin/env python3

from sqlalchemy import (create_engine, Column, Integer, String, DateTime, CheckConstraint, Index, update)
from sqlalchemy.orm import sessionmaker, validates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, timedelta
import random

Base = declarative_base()

# Define a Videogame model class
class Videogame(Base):
    __tablename__ = 'videogames'

    Index('index_name', 'title')

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False) # adds database constraint so that this column can never contain null values
    studio = Column(String())
    genre = Column(String())
    # use CheckConstraint class to add a custom constraint to this column
    release_year = Column(Integer(), CheckConstraint('release_year >= 1998 AND release_year <= 2018'))
    release_date = Column(DateTime())

    # can use the optional class attr 'table_args' to store constraints for multiple columns
    __table_args__ = (
        CheckConstraint('release_year >= 1998 AND release_year <= 2018'),
    )

    def __repr__(self):
        return f"Videogame {self.id}: " \
            + f"Title: {self.title}, " \
            + f"Studio: {self.studio}, " \
            + f"Genre: {self.genre}, " \
            + f"Release: {self.release_year}"

if __name__ == '__main__':

    # Create a connection to the SQLite database
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a new videogame
    mario_odyssey = Videogame(title='Super Mario Odyssey', studio='Nintendo', genre='Platformer', release_year=2017, release_date=date(2017, 10, 27))
    session.add(mario_odyssey)
    zelda = Videogame(title="The Legend of Zelda: Ocarina of Time", studio="Nintendo", genre="Action-Adventure", release_year=1998, release_date=date(1998, 11, 21))
    session.add(zelda)
    session.commit()

    # Read all videogames in the database
    # videogames = session.query(Videogame)
    # print([game for game in videogames])
    videogames = session.query(Videogame).all()
    for game in videogames:
        print(game)

    videogame = session.query(Videogame).filter_by(id=1).first()
    videogame.title = "A New Title"
    session.commit()

    videogame = session.query(Videogame).filter_by(id=1).first()
    print(f"Updated game: {videogame}")

    # Update the second videogame title using the update() method with error and handling
    update_query = update(Videogame).where(Videogame.id == 2).values(title="Another New Title", release_year=2019)
    try:
        session.execute(update_query)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()

    # requery the same game to verify the update
    videogame = session.query(Videogame).filter_by(id=2).first()
    print(f"Updated game: {videogame}")


   