from ..config import sqlalchemy_uri


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(sqlalchemy_uri())

Session = sessionmaker(engine)
