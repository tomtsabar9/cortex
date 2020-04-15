import sqlalchemy as db


def get_table(metadata, name):

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
              )

