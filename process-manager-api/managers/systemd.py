import managers
from managers import ProcessModel


class Systemd(managers.ProcessManagerProtocol):
    def start(self, process: ProcessModel):
        pass

    def stop(self, process: ProcessModel):
        pass

    def status(self, process: ProcessModel):
        pass

    def enable(self, process: ProcessModel):
        pass

    def disable(self, process: ProcessModel):
        pass

    def reload_daemon(self):
        pass

    def view_logs(self, process: ProcessModel):
        pass
