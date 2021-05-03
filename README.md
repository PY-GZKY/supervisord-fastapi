[![](https://github.com/augustoliks/supervisord-fastapi/actions/workflows/docker-build.yml/badge.svg)](https://github.com/augustoliks/supervisord-fastapi/actions/workflows/docker-build.yml)
[![augustoliks/supervisord-fastapi](https://img.shields.io/badge/dockerfile-augustoliks/supervisord--fastapi:latest-blue.svg)](https://hub.docker.com/r/augustoliks/supervisord-fastapi)
[![Docker Pulls](https://img.shields.io/docker/pulls/augustoliks/supervisord-fastapi.svg)](https://hub.docker.com/r/augustoliks/supervisord-fastapi/)

# supervisord-fastapi

*[Supervisord](https://github.com/Supervisor/supervisor) + [FastAPI](https://github.com/tiangolo/fastapi) = supervisord-fastapi* :smile: :rocket:

HTTP API to connect [Supervisord](https://github.com/Supervisor/supervisor) main functions.

Features: 

- List process info;
- Start process;
- Stop process;
- Restart process;
- Reload Supervisord Configuration.

## Quick Start

### Running with Docker :whale:

To run `supervisord-fastapi` in container, it's needed declare `VOLUME (-v)` to Unix Domain Socket File of Supervisord XML-RPC API.

```shell
$ docker pull augustoliks/supervisord-fastapi:latest
$ docker run -it -p 5000:5000 -v /var/run/supervisor/supervisor.sock:/var/run/supervisor/supervisor.sock augustoliks/supervisord-fastapi:latest
```

### Running with CLI :computer: 

Prerequisites: 

Dependency          | Version
---                 |---
python              | >= 3.5
pip                 | >= 9.0.1
supervisor          | >= 4.2.1 

If necessary, upgrade your version of pip:

```shell
$ python3 -m pip install --upgrade pip
```

If you cannot upgrade pip due to a system-owned installation, you can run the example in a virtualenv:

```shell
$ python -m pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ python -m pip install --upgrade pip
```

Download Project:

```shell
$ git clone https://github.com/augustoliks/supervisord-fastapi
```

Install Dependencies:

```shell
$ pip3 install -r requirements.txt
```

Run application:

```shell
$ cd src/
$ uvicorn --port 5000 entrypoint:create_app 
```

## Configuration

The configuration is made through *Environment Variables*. If necessary, override values.

Environment Variable                | Description                                           | Default Value
---                                 |---                                                    |---
`SUPERVISORD_ADDRESS_HTTP`          | HTTP Address to access Supervisord instance           | `http://localhost`
`SUPERVISORD_ADDRESS_UNIX_SOCKET`   | Unix Domain Socket File of Supervisord XML-RPC API    | `/var/run/supervisor/supervisor.sock`
`TZ`                                | Host Timezone                                         | `America/Sao_Paulo`
