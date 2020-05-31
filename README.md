[![Build Status](https://travis-ci.org/tomtsabar9/cortex.svg?branch=master)](https://travis-ci.org/tomtsabar9/cortex)[![codecov](https://codecov.io/gh/tomtsabar9/cortex/branch/master/graph/badge.svg)](https://codecov.io/gh/tomtsabar9/cortex)

# cortex

Final project in "Advanced System Design" course.

You are more than welcome to follow my progress on Trello https://trello.com/b/7jks3j5q/cortex.

See documentation in https://cortex-project.readthedocs.io/en/latest/.

## Overview
The project holds 9 microservices:
1. Client that uploads cortex data of some users.
2. Server that get data from users and pass it through queue to the parsers.
3. RabbitMQ.
4. Parsers that parse the data and pass it through queue to the savers.
5. Savers that save the parsed data in a database.
6. The DB.
7. API that responsible for comfortable interface for developers.
8. CLI that consumes the API, mostly for debuging.
9. GUI that responsible for viewing everything nicely 

![Image of system](https://raw.githubusercontent.com/tomtsabar9/cortex/master/system.png)


## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:tomtsabar9/cortex.git
    ...
    $ cd cortex/
    ```
2. Run the installation script and activate the virtual environment:
    ```sh
    $ sudo ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [cortex] $ 
    ```

3. Run the tests, just to make sure:
    ```sh
    $ pytest
    ```


## Usage
### Fast usage:

Download a sample and put it in:
\cortex\sample.mind.gz


```sh
$ sudo . ./scripts/run_pipeline.sh <email> <password>
```
This will run two scripts:
    1. ./scripts/start_dockers.sh
    2. ./scripts/start_micro_services.sh

The first will install and run the dockers, it works independently and both for first try or later.
The second is just a shortcut for running all the microservices in different terminals, made for convenient.
This quick start will allow you to fastly activate the project.

### Client Usage:

Just surf with your favorite web browser to http://localhost:8080.
Have fun ;)

### Dev-op Usage:

#### RabbitMQ:
Surf to http://localhost:15672/, use the same username and password you supplied.
#### Postgres admin:
Surf to http://localhost, use the same username and password you supplied.
Due to inner problem with posgres-admin,in order to connect to the database you must either of outer computers IP or docker IP.
Something wrong with 127.0.0.1/localhost. The username and password for the database are them same as to the administrative website.
#### API:
Surf to http://localhost:5000/users as good starting position.

### Independent run:

When running independently you should export yourself the username and password:
bash:
```sh
$  export _USERNAME=<username>
$  export _PASSWORD=<password>
```

Start with exporting the enc variables of username and password.
Each of the microservices can be run independently of the other, in two different ways:
1. From the command line
2. By importing its module in python
The following will demonstrate how to use each of the microservices:
> Most of the parameters have default values. The server for example can be run as "python -m cortex.server run-server". The following demonstrate usage of all parameters.

#### Client:
bash:
```sh
$  python -m cortex.client upload-sample --host '127.0.0.1' --port 8000 <sample_path.gz>
```

python:
```pycon
>>> from cortex.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
```
#### Server:
bash:
```sh
$  python -m cortex.server run-server --host '127.0.0.1' --port 8000 'rabbitmq://127.0.0.1:5672/'
```

python:
```pycon
>>> from cortex.server import run_server
>>> run_server(host='127.0.0.1', port=8000, publish=print)
```

#### Parsers:
bash:
```sh
$  python -m cortex.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
```

or for parsing raw data from file
```sh
$  python -m cortex.parsers parse 'pose' '<path>'
```
python:
```pycon
>>> from cortex.parsers import run_parser
>>> run_parser(name='pose', queue_url='rabbitmq://127.0.0.1:5672/')
```
or 
```pycon
>>> from cortex.parsers import parse
>>> data = ...
>>> parse('pose', data)
    ```
#### Saver:
bash:
```sh
$  python -m cortex.saver run-saver 'postgresql://127.0.0.1:5432' 'rabbitmq://127.0.0.1:5672/'
```

or for saving raw data from file
```sh
$ python -m cortex.saver save --database 'postgresql://127.0.0.1:5432' 'pose' '<path>'
```

python:
```pycon
>>> from cortex.saver import run_saver
>>> run_saver(db_url='postgresql://127.0.0.1:5432', queue_url='rabbitmq://127.0.0.1:5672/')
```
or 
```pycon
>>> from cortex.saver import save
>>> data = …
>>> save('postgresql://127.0.0.1:5432', 'pose', data)
```
#### API:
bash:
```sh
$  python -m cortex.api run-server --host '127.0.0.1' --port 5000 --database 'postgresql://127.0.0.1:5432'
```

python:
```pycon
>>> from cortex.api import run_api_server
>>> run_api_server(host = '127.0.0.1', port = 5000, database_url = 'postgresql://127.0.0.1:5432')
```

#### CLI:
bash:
```sh
$  python -m cortex.cli get-users
…
$ python -m cortex.cli get-user 42
…
$ python -m cortex.cli get-snapshots 42
…
$ python -m cortex.cli get-snapshot 42 AABBCCDDEE
…
$ python -m cortex.cli get-result 42 AABBCCDDEE 'pose'
```
#### GUI:
bash:
```sh
$  python -m cortex.gui run-server --host '127.0.0.1' --port 8080 --api-host '127.0.0.1' --api-port 5000
```

python:
```pycon
>>> from cortex.gui import run_server
>>> run_server(host = '127.0.0.1', port = 8080, api_host = '127.0.0.1', api_port = 5000)
```

## Intergration

### Adding a parser

There exists two kinds of parser - image and regular.
In order to add another parsers just go to the parsers.py file, add a parser function with one data argumant and simple return value. Add the @parser('new_parser') decorator to finish the job. As seen in the 'pose' parser the return value is the parsed data.

```python
@parser('pose')
def parse_pose(data):

        
    pose = PoseMsg()
    pose.ParseFromString(data)

    pose_json = json.dumps(dict(
            px = pose.translation.x,
            py = pose.translation.y,
            pz = pose.translation.z,
            rx = pose.rotation.x,
            ry = pose.rotation.y,
            rz = pose.rotation.z,
            rw = pose.rotation.w
            ))
    return pose_json
```

The image parser is a little bit more complected, it saves the image in a temporary location and return its path.
The wrapper responsible for moving the temporary image file to the right location.

```python
@parser('color_image')
def parse_color_image(data):
        

    color_image = ColorImageMsg()
    color_image.ParseFromString(data)

    image = Image.frombytes("RGB", (color_image.width, color_image.height), color_image.data, 'raw')

    tmp_file = tempfile.NamedTemporaryFile()                
    path_str = tmp_file.name
    tmp_file.close()

    image.save(path_str, 'png')
    return path_str
```




