import importlib
import managers
from settings import settings


def invoke_process_manager() -> managers.ProcessManagerProtocol:
    type_, props = settings.metrics
    cls = getattr(importlib.import_module('metrics'), type_)
    return cls(**props)


singleton_process_manager = invoke_process_manager()
