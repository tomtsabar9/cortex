import sqlalchemy as db


def get_table(metadata, name):
  """
  Wraps usage of database tables so they can be managed from one place.
  """
  if name == "users":
    return db.Table('users', metadata,
              db.Column('Id', db.BigInteger(), primary_key=True),
              db.Column('Name', db.String() , nullable=False),
              db.Column('Birth', db.Integer()),
              db.Column('Gender', db.CHAR()),
              )
  elif name == "snapshots":
    return db.Table('snapshots', metadata,
              db.Column('Uid', db.String(), primary_key=True, nullable=False),
              db.Column('Id', db.BigInteger()),
              db.Column('Date', db.BigInteger()),
              db.Column('Results', db.String(), nullable=False),
              )
  else:
    return db.Table(name, metadata,
              db.Column('Id', db.Integer()),
              db.Column('Date', db.BigInteger() , nullable=False),
              db.Column('Data', db.String()),
              )
