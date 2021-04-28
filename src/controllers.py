import typing
import supervisord
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


def exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def internal_server_error(request, exc):
        return PlainTextResponse(str(exc), status_code=500)


def supervisord_routes(app: FastAPI):
    supervisord_daemon = supervisord.Supervisord()

    @app.get("/info/", response_model=typing.List[supervisord.ProcessInfo])
    async def get_info_all_process():
        """get information of all process"""
        return supervisord_daemon.all_process_info()

    @app.get("/info/{process_name}", response_model=supervisord.ProcessInfo)
    async def get_info_process(process_name: str):
        """get information process"""
        return supervisord_daemon.process_info(process_name)

    @app.post("/restart/{process_name}", response_model=supervisord.ProcessInfo)
    async def restart_process(process_name: str):
        """restart process"""
        supervisord_daemon.restart(process_name)
        return supervisord_daemon.process_info(process_name)

    @app.post("/start/{process_name}", response_model=supervisord.ProcessInfo)
    async def start_process(process_name: str):
        """start process"""
        supervisord_daemon.start(process_name)
        return supervisord_daemon.process_info(process_name)

    @app.post("/stop/{process_name}", response_model=supervisord.ProcessInfo)
    async def stop_process(process_name: str):
        """stop process"""
        supervisord_daemon.stop(process_name)
        return supervisord_daemon.process_info(process_name)


def create_app():
    app = FastAPI()
    supervisord_routes(app)
    exception_handlers(app)
    return app
