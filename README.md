# bcg-test

The command line interface to this app is provided via Makefile targets. To view all the available 
command line options run `make help` in the root of the repo.

The application is fully dockerised so you do not need any specific local python
environment setup for it to work. 

## Install and Run

### Docker
In order to install the application you will need docker and docker compose running locally.
To install these dependencies follow instructions here
  - https://docs.docker.com/docker-for-mac/install/

### BCG application
To install and run the application simply run:
```
make start
```
Or to run in the background use:
```
make start-detached
```
To make an example request to the API you can run the following. Please 
bear in mind that the API takes a few seconds to start up and migrate the 
database. Therefore the request will fail before the app is fully ready.
```
make example-post-to-payments-api
```


## Development
### Testing
To run the test suite
```
make test
```

### Linting
To run linting
```
make lint
```
