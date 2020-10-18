from fastapi import FastAPI
import services


def controllers(app: FastAPI):
    manager_process_service = services.ManagerProcess()

    @app.get('/list-process')
    def list_all_process() -> None:
        pass

    @app.get('/list-units')
    def list_all_process():
        pass

    @app.get('/start')
    def start_process(process_id: str):
        pass

    @app.get('/stop')
    def stop_process(process_id: str) -> None:
        pass

    @app.get('/restart')
    def restart_process(process_id: str) -> None:
        process_id
        manager_process_service.restart_process(process_id)

    @app.get('/enable')
    def enable_process(process_id: str):
        pass

    @app.get('/disable')
    def disable_process(process_id: str):
        pass


def run():
    app = FastAPI()
    controllers(app)
