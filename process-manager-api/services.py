import managers
import singletons as di


class ManagerProcess:
    def __init__(
        self,
        process_manager: managers.ProcessManagerProtocol = di.singleton_process_manager
    ):
        self.process_manager = process_manager

    def restart_process(self, process: managers.ProcessModel):
        self.process_manager.stop(process)
        self.process_manager.start(process)

    def list_all_process(self, process: managers.ProcessModel):
        self.process_manager.stop(process)
        self.process_manager.start(process)
