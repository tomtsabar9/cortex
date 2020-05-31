from .. import Connection
import sys
import gzip
import struct
import click
import requests 

URL = 'http://<ip>:<port>/'

@click.group()
@click.option('-h', '--host', default="127.0.0.1", help='server\'s ip')
@click.option('-p', '--port', default=5000, help='server\'s port')
def reflect(host, port):
    """
    Just a grouping for other commands
    """
    global URL
    URL = URL.replace('<ip>', host).replace('<port>', str(port))
   
@reflect.command()
def get_users():
    
    users_url = URL + "users"
    # sending get request and saving the response as response object 
    r = requests.get(url = users_url, timeout=3) 
  
    # extracting data in json format 
    data = r.json() 
    print (data)

@reflect.command()
@click.argument('user-id')
def get_user(user_id):
    user_url = URL + 'users/' + user_id
    # sending get request and saving the response as response object 
    r = requests.get(url = user_url, timeout=3) 
  
    # extracting data in json format 
    data = r.json() 
    print (data)

@reflect.command()
@click.argument('user-id')
def get_snapshots(user_id):
    snapshots_url = URL + 'users/' + user_id + '/snapshots'
    # sending get request and saving the response as response object 
    r = requests.get(url = snapshots_url, timeout=3) 
  
    # extracting data in json format 
    data = r.json() 
    print (data)

@reflect.command()
@click.argument('user-id')
@click.argument('snapshot-id')
def get_snapshot(user_id, snapshot_id):
    snapshot_url = URL + "users/" + user_id + "/snapshots/" + snapshot_id
    # sending get request and saving the response as response object 
    r = requests.get(url = snapshot_url, timeout=3) 
  
    # extracting data in json format 
    data = r.json() 
    print (data)

@reflect.command()
@click.argument('user-id')
@click.argument('snapshot-id')
@click.argument('result')
def get_result(user_id, snapshot_id, result):
    result_url = URL + "users/" + user_id + "/snapshots/" + snapshot_id + "/" +result
    # sending get request and saving the response as response object 
    r = requests.get(url = result_url, timeout=3) 
    
    # extracting data in json format 
    data = r.text 
    print (data)

if __name__ == '__main__':
    reflect()

