import json
import sqlalchemy as db
from sqlalchemy.sql import text
from sqlalchemy.sql import select

from .. import get_table

from pathlib import Path
import flask



def create_api(db_url):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    cortex_db = db.create_engine(db_url)

    @app.route('/users', methods=['GET'])
    def users():
        connection = cortex_db.connect()
        metadata = db.MetaData()

        users_table = get_table(metadata, 'users')


        user_dict = dict()
        s = select([users_table])
        for user in connection.execute(s).fetchall():
            user_dict[user[0]] = user[1]
        return json.dumps(user_dict)

    @app.route('/users/<user_id>', methods=['GET'])
    def user(user_id):
        connection = cortex_db.connect()
        metadata = db.MetaData()
        users_table = get_table(metadata, 'users')

        s = select([users_table]).where(users_table.c.Id == int(user_id))

        return json.dumps(list(connection.execute(s).fetchall()[0]))

    @app.route('/users/<user_id>/snapshots', methods=['GET'])
    def snapshots(user_id):
        connection = cortex_db.connect()
        metadata = db.MetaData()
        snapshots_table = get_table(metadata, 'snapshots')

        s = select([snapshots_table]).where(snapshots_table.c.Id == int(user_id))

        snaptshot_dict = dict()

        for entry in connection.execute(s).fetchall():
            snaptshot_dict[entry[0]] = entry[2]

        return json.dumps(snaptshot_dict)

    @app.route('/users/<user_id>/snapshots/<snapshot_uid>', methods=['GET'])
    def snapshot(user_id, snapshot_uid):
        connection = cortex_db.connect()
        metadata = db.MetaData()
        snapshots_table = get_table(metadata, 'snapshots')

        
        s = select([snapshots_table]).where(snapshots_table.c.Uid == snapshot_uid)

        snapshot = connection.execute(s).fetchall()[0]

        return json.dumps([snapshot[0], snapshot[2], snapshot[3]])

    @app.route('/users/<user_id>/snapshots/<snapshot_uid>/<result>', methods=['GET'])
    def get_result(user_id, snapshot_uid, result):
        connection = cortex_db.connect()
        metadata = db.MetaData()

        snapshots_table = get_table(metadata, 'snapshots')
        
        s = select([snapshots_table]).where(snapshots_table.c.Uid == snapshot_uid)

        datetime = connection.execute(s).fetchall()[0][2]

        result_table = get_table(metadata, result)
        
        s = select([result_table]).where(result_table.c.Id == int(user_id)).where(result_table.c.Date == int(datetime))

        data = connection.execute(s).fetchall()[0][2]

        return data

    @app.route('/users/<user_id>/snapshots/<snapshot_uid>/<result>/data', methods=['GET'])
    def get_result_data(user_id, snapshot_uid, result):
        
        path = Path(get_result(user_id, snapshot_uid, result))

        print (path.parent, path.name)
        return flask.send_from_directory(directory=path.parent, filename=path.name)

    return app



