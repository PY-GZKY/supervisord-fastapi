import importlib
import sys
from pathlib import Path

from loguru import logger

import managers
from settings import settings


def setup_log(
        id_instance='fs-sender',
        level='TRACE',
        directory=None,
        log_format='<fg #A8A8A8>{time:YYYY-MM-DD : HH:mm:sss}</fg #A8A8A8> '
                   '| {thread.name} '
                   '| <lvl>{level}</lvl> '
                   '| <green>{message}</green>'
):
    logger.remove()
    logger.add(sys.stderr, level=level, format=log_format)
    if directory:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.add(
            Path(directory, f'{id_instance}-{level}.log'),
            level=level,
            format=log_format
        )


def invoke_process_manager() -> managers.ProcessManagerProtocol:
    type_, props = settings.metrics
    cls = getattr(importlib.import_module('metrics'), type_)
    return cls(**props)


try:
    setup_log(id_instance=settings.integration_type, **settings.log)
except Exception as e:
    setup_log()
    logger.warning(e)

singleton_process_manager = invoke_process_manager()
