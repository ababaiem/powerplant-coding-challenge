# Powerplant Coding Challenge
## Introduction

This app computes the distribution of power for the engie powerplant-challenge using `Python 3.8+` and `flask`.
The entire code is located in the `app.py` file. This guide assumes that you are working with a Unix system, i.e. macOS or GNU/Linux.

## Requirements

Make sure to have `Python 3.8+`, `flask` and `docker` installed. The details can be found in the `requirements.txt` file.
I tested the app using the latest version of [Postman](https://www.postman.com/downloads/).

## Setup

Clone the repository from GitHub and enter the project directory:

```
$ git clone https://github.com/ababaiem/powerplant-coding-challenge.git
$ cd powerplant-coding-challenge/
```

Set up a new virtual environment, activate it and install the minimum requirements:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Running the app

### Localy
Run the application on the production server :  
`python3 app.py`  

The API will be listening on the port `8888` from `localhost` at:
`http://localhost:8888/productionplan`  

### Docker

Install [Docker](https://www.docker.com/) depending on your OS.

In the root folder, build the application image by running the following command :  
`docker build --tag powerplant .` 

It will create an image called `powerplant`.

Create and start a Docker container based on the powerplant image :  
`docker run -d -p 8888:8888 powerplant`  

It will start the application in a container available on port `8888`. API will be listening at :  
`http://localhost:8888/productionplan` 

### Send payload

You may use `Postman` and use it to send payload or, you can also submit a chosen payload by using the following CURL command:
`curl -X POST -d @doc/example_payloads/payload1.json -H "Content-Type: application/json" http://localhost:8888/productionplan`