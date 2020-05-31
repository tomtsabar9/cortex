[![Build Status](https://travis-ci.org/tomtsabar9/cortex.svg?branch=master)](https://travis-ci.org/tomtsabar9/cortex)[![codecov](https://codecov.io/gh/tomtsabar9/cortex/branch/master/graph/badge.svg)](https://codecov.io/gh/tomtsabar9/cortex)

# cortex

Final project in "Advanced System Design" course.

You are welcome to follow my progress on Trello https://trello.com/b/7jks3j5q/cortex.

See documentation in https://cortex-project.readthedocs.io/en/latest/.

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:tomtsabar9/cortex.git
    ...
    $ cd cortex/
    ```
2. Run the installation script and activate the virtual environment:
	```
    ...
    $ sudo ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [cortex] $ 
    ```

3. Run the tests, just to make sure:
    ```
    $ pytest
    ```


## Usage
### First usage:

    ```sh
    $ sudo ./scripts/run_pipeline.sh
    ```
This will run two scripts:
	1. ./scripts/start_dockers.sh
	2. ./scripts/start_micro_services.sh

The first will install and run the dockers, it works independently and both for first try or later.
The second is just a shortcut for running all the microservices in different terminals, made for convenient.
This quick start will allow you to fastly activate the project.

### Client Usage:

Just surf your favorite web browser to http://localhost:8080.
Have fun ;)

### Dev-op Usage:

#### RabbitMQ:
Surf to http://localhost, use the same username and password you supplied
#### Postgres admin:
Surf to http://localhost, use the same username and password you supplied.
Due to inner problem with posgres-admin,in order to connect to the database you must either of outer computers IP or docker IP.
Something wrong with 127.0.0.1/localhost. The username and password for the database are them same as to the administrative website.
#### API:
Surf to http://localhost:5000/users as good starting position.

### Independent run:

Each of the microservices can be run independently of the other in two manners:
1. From the command line
2. By importing its module in python
The following will demonstrate how to use each of the microservices:

#### Client:
#### Server:
#### Parsers:
#### Saver:
#### API:
#### CLI:
#### GUI:

## Intergration

### Ading a parser




