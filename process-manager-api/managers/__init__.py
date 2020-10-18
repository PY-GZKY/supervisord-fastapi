import abc
import pydantic


class ProcessModel(pydantic.BaseModel):
    process_id: str


class ProcessManagerProtocol(abc.ABC):
    @abc.abstractmethod
    def start(self, process: ProcessModel):
        pass

    @abc.abstractmethod
    def stop(self, process: ProcessModel):
        pass

    @abc.abstractmethod
    def status(self, process: ProcessModel):
        pass

    @abc.abstractmethod
    def enable(self, process: ProcessModel):
        pass

    @abc.abstractmethod
    def disable(self, process: ProcessModel):
        pass

    @abc.abstractmethod
    def view_logs(self, process: ProcessModel):
        pass

    @abc.abstractmethod
    def reload_daemon(self):
        pass
