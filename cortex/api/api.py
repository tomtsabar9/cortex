import json
import sqlalchemy as db
from sqlalchemy.sql import text
from sqlalchemy.sql import select

from .. import get_table

from pathlib import Path
import flask
from flask_cors import cross_origin



def create_api(db_url):
    """
    Returns an flask appication the runs the api.
    The api reads directly from the database, parses the data serves it to the clinet, 
    """
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    cortex_db = db.create_engine(db_url)

    @app.route('/users', methods=['GET'])
    def users():
        """
        Returns json of all the clients with their ids.
        """
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
        """
        Returns json of all the details specific user.
        """
        connection = cortex_db.connect()
        metadata = db.MetaData()
        users_table = get_table(metadata, 'users')

        s = select([users_table]).where(users_table.c.Id == int(user_id))

        return json.dumps(list(connection.execute(s).fetchall()[0]))

    @app.route('/users/<user_id>/snapshots', methods=['GET'])
    def snapshots(user_id):
        """
        Returns json of all the snapshots of specific user.
        """
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
        """
        Returns json of all the results exists in a single snapshot.
        """
        connection = cortex_db.connect()
        metadata = db.MetaData()
        snapshots_table = get_table(metadata, 'snapshots')

        
        s = select([snapshots_table]).where(snapshots_table.c.Uid == snapshot_uid)

        snapshot = connection.execute(s).fetchall()[0]

        print (snapshot[3])
        snap_json = dict()
        snap_json['id'] = snapshot[0]
        snap_json['time'] = snapshot[2]
        snap_json['options'] = json.loads(snapshot[3])

        return json.dumps(snap_json)

    @app.route('/users/<user_id>/snapshots/<snapshot_uid>/<result>', methods=['GET'])
    @cross_origin(origin='*')
    def get_result(user_id, snapshot_uid, result):
        """
        Returns json of a single results within a snapshot.
        """
        connection = cortex_db.connect()
        metadata = db.MetaData()

        snapshots_table = get_table(metadata, 'snapshots')
        
        s = select([snapshots_table]).where(snapshots_table.c.Uid == snapshot_uid)

        datetime = connection.execute(s).fetchall()[0][2]

        result_table = get_table(metadata, result)
        
        s = select([result_table]).where(result_table.c.Id == int(user_id)).where(result_table.c.Date == int(datetime))

        data = connection.execute(s).fetchall()[0][2]

        return str(data)

    @app.route('/users/<user_id>/snapshots/<snapshot_uid>/<result>/data', methods=['GET'])
    def get_result_data(user_id, snapshot_uid, result):
        """
        Returns an actual image (instead of a path).
        """
        temp = get_result(user_id, snapshot_uid, result)
        path = Path(temp.response[0].decode('ascii'))
       
        print (path.parent,path.name)
        return flask.send_from_directory(directory=path.parent, filename=path.name)

    return app



