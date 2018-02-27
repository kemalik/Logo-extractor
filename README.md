# Logo-extractor
Logo extractor is thr web service for extract site logotype

## Installation
First, [install Docker](https://docs.docker.com/installation/). If you're new to Docker, you might also want to check out the [Hello, world! tutorial](https://docs.docker.com/userguide/dockerizing/).

Next, clone this repo:

    $ git clone https://github.com/kemalik/Logo-extractor.git
    $ cd Logo-extractor

## Configure the project

Project settings live in `.env`. It contains sensitive data, so it's excluded in `.gitignore` and `.dockerignore`. Copy `.env.sample` to `.env`:

    $ cp .env.sample .env

Edit `.env`. At a minimum, change these settings:

* `SECRET_KEY`: this is the secret key for a Django project. You can generate [here](https://www.miniwebtool.com/django-secret-key-generator/).
* `MYSQL_ROOT_PASSWORD`: this is the password for a mysql `root` user. Change it to something secure.

## Build and Run
Build the Docker image (you should be in the `Logo-extractor/` directory, which contains the `Dockerfile`):

    $ docker build -t <yourname>/logo-extractor .
    
Run the needed Docker images with [docker-compose](https://docs.docker.com/compose/):

    $ docker-compose up -d 
Open [http://localhost:8000/?url=http://google.com](http://localhost:8000/?url=http://google.com) in a browser. You should see a extracted logo of [Google](https://google.com).

![result page](https://preview.ibb.co/nptWyH/logo_extractor.png)