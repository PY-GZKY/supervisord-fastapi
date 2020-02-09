# supervisord-integrated-fast-api

Simple HTTP-API for manage Supervisord Units.

## Run App

- Go to project source code

```shell script
cd src
```

- Installation of Dependencies

```shell script
pip3.7 install -r requirements.txt
```

- Run Application
```shell script
uvicorn main:app --reload
```

---


One the way to execute this project, is run _shell-script_ `run.sh`

```shell script
cd src
chmod +x run.sh
sh run.sh
```