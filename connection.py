import psycopg2
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

_engine     = None
_session    = None

def connect(args = None):
    engine(args)
    session()
    return _engine, _session

def engine(args = None):
    global _engine
    if _engine is None:
        if args and args.url:
            url = args.url
        else:
            url = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
        _engine  = sa.create_engine(url)
    return _engine

def session():
    global _session
    if _session is None:
        _session = orm.sessionmaker(bind=engine())()
    return _session