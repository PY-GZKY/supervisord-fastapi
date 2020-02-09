from fastapi import FastAPI
from supervisor import Supervisor


app = FastAPI()
supervisor = Supervisor()


@app.get('/list-process')
def list_all_process() -> None:
    return supervisor.units


@app.get('/list-units')
def list_all_process():
    return supervisor.process


@app.get('/start')
def start_process(process_id: str):
    supervisor.start(process_id)


@app.get('/stop')
def stop_process(process_id: str) -> None:
    supervisor.stop(process_id)


@app.get('/restart')
def restart_process(process_id: str) -> None:
    supervisor.restart(process_id)


@app.get('/enable')
def enable_process(process_id: str):
    supervisor.enable_unit(process_id)
    supervisor.update()


@app.get('/disable')
def disable_process(process_id: str):
    supervisor.disable_unit(process_id)
    supervisor.update()
