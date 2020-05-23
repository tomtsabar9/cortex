from pathlib import Path
import flask
from flask import request
import requests
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

def run(host, port, api_host, api_port):
    """
    
    """

    gui = create_gui(api_host, api_port)  
    gui.run(host=host, port=port)

def create_gui(api_host, api_port):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config["DEBUG"] = True
    url = 'http://'+api_host+":"+str(api_port)
   

    @app.route('/', methods=['GET'])
    def welcome():
        r = requests.get(url+'/users')


        return render_template('users.html', users = r.json().items())


    @app.route('/show/<user_id>', methods=['GET'])
    def show(user_id):
        r = requests.get(url+'/users/'+user_id+'/snapshots')

        
        snapshots = list(r.json().items())

        snapshots_full_data = []

        for snapshot in snapshots:
            snapt_dict=dict()

            snapshots_options = requests.get(url+'/users/'+user_id+'/snapshots/'+snapshot[0]).json()

            options = snapshots_options['options']

            snapt_dict['time'] = str(snapshot[1])
            snapt_dict['id'] = str(snapshot[0])
            
            for option in options:
                snapt_dict[option] = url+'/users/'+user_id+'/snapshots/'+snapshot[0]+"/"+option

            snapshots_full_data.append(snapt_dict)

            

        return render_template('show.html', snapshots = json.dumps(snapshots_full_data), user_name=request.args['user_name'])

    return app