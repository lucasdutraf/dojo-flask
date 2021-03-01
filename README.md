# dojo-flask
A simple todo API built with Flask, written as a tutorial.

## Installation
Docker and docker-compose are required.

Before building the container, allow execution of the entrypoint script:

    chmod +x entrypoint.sh

Then:
    
    sudo docker-compose -f docker-compose-dev.yml up --build
    
The api will be running at localhost:5001.

## Tests
Running tests:  

    `sudo docker-compose -f docker-compose-dev.yml run api python manage.py test`