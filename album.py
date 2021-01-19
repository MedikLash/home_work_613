import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH="sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    
    docstring
    """
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save_data(new_artist):
    new_write = Album(year=new_artist['year'], artist=new_artist['artist'], genre=new_artist['genre'], album=new_artist['album'])
    session = connect_db()
    session.add(new_write)
    session.commit()