# supervisord-fastapi

Supervisord + FastAPI = *supervisord-fastapi* :smile: :rocket:

Web-API to manage [Supervisord](https://github.com/Supervisor/supervisor) main functions.

Features: 

- List process info;
- Start process;
- Stop process;
- Restart process;
- Reload Supervisord Configuration.

## Quick Start

Prerequisites: 

Dependency          | Version
---                 |---
python              | >= 3.
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

Environment Variable                | Description                                   | Default Value
---                                 |---                                            |---
`SUPERVISORD_ADDRESS_HTTP`          | HTTP Address to access Supervisord instance   | `http://localhost`
`SUPERVISORD_ADDRESS_UNIX_SOCKET`   | Unix Socket to Supervisord XML-RPC API        | `/var/run/supervisor/supervisor.sock`
