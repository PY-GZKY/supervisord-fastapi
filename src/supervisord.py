import os
import socket
import pathlib
import typing
from xmlrpc import client
from http.client import HTTPConnection
import datetime
from pydantic import (
    BaseModel,
    Field
)


SUPERVISORD_ADDRESS_HTTP = os.getenv(
    'SUPERVISORD_ADDRESS_HTTP',
    'http://localhost'
)
SUPERVISORD_ADDRESS_UNIX_SOCKET = os.getenv(
    'SUPERVISORD_ADDRESS_UNIX_SOCKET',
    '/var/run/supervisor/supervisor.sock'
)


class SupervisordProcessStates:
    """High Level Supervisord Process States

    A process controlled by supervisord will be in one of the below states at any given time.
    You may see these state names in various user interface elements in clients.

    Reference: http://supervisord.org/subprocess.html#process-states
    """

    STOPPED = 0
    """The process has been stopped due to a stop request or has never been started"""
    STARTING = 10
    """The process is starting due to a start request"""
    RUNNING = 20
    """The process is running"""
    BACKOFF = 30
    """
    The process entered the STARTING state but subsequently 
    exited too quickly (before the time defined in startsecs) to move to the RUNNING state
    """
    STOPPING = 40
    """The process is stopping due to a stop request"""
    NOT_RUNNING = 70
    """Process is not running"""
    ALREADY_STARTED = 60
    """Process already started and running"""
    EXITED = 100
    """The process exited from the RUNNING state (expectedly or unexpectedly)"""
    FATAL = 200
    """The process could not be started successfully"""
    UNKNOWN = 1000
    """The process is in an unknown state (supervisord programming error)"""


class ProcessInfoState:
    """
    This is an internal value maintained by Supervisor that determines what Supervisor believes to be its current operational state.
    """

    FATAL = 2
    """Supervisor has experienced a serious error"""
    RUNNING = 1
    """Supervisor is working normally"""
    RESTARTING = 0
    """Supervisor is in the process of restarting"""
    SHUTDOWN = -1
    """Supervisor is in the process of shutting down"""


class ProcessInfo(BaseModel):
    name: str = Field(
        description="Name of the process"
    )
    group: str = Field(
        description="Name of the process’ group"
    )
    description: str = Field(
        description=(
            "If process state is running description’s value is process_id and uptime. "
            "Example “pid 18806, uptime 0:03:12 ”. If process state is stopped description’s value is stop time. "
            "Example:”Jun 5 03:16 PM ”."
        )
    )
    start: datetime.datetime = Field(
        description="UNIX timestamp of when the process was started"
    )
    stop: datetime.datetime = Field(
        description="UNIX timestamp of when the process last ended, or 0 if the process has never been stopped."
    )
    now: datetime.datetime = Field(
        description="UNIX timestamp of the current time, which can be used to calculate process up-time."
    )
    state: int = Field(
        description="State code, see Process States."
    )
    statename: str = Field(
        description="String description of state, see Process States."
    )
    logfile: pathlib.Path = Field(
        description=(
            "Deprecated alias for stdout_logfile. "
            "This is provided only for compatibility with clients written for Supervisor 2.x and may be removed "
            "in the future. Use stdout_logfile instead."
        )
    )
    stdout_logfile: pathlib.Path = Field(
        description="Absolute path and filename to the STDOUT logfile"
    )
    stderr_logfile: pathlib.Path = Field(
        description="Absolute path and filename to the STDOUT logfile"
    )
    spawnerr: str = Field(
        description="Description of error that occurred during spawn, or empty string if none."
    )
    exitstatus: int = Field(
        description="Exit status (errorlevel) of process, or 0 if the process is still running."
    )
    pid: int = Field(
        description="UNIX process ID (PID) of the process, or 0 if the process is not running."
    )


class UnixStreamHTTPConnection(HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.host)


class UnixStreamTransport(client.Transport):
    def __init__(self, socket_path):
        self.socket_path = socket_path
        super(UnixStreamTransport, self).__init__()

    def make_connection(self, host):
        return UnixStreamHTTPConnection(self.socket_path)


class Supervisord:
    def __init__(
            self,
            address=SUPERVISORD_ADDRESS_HTTP,
            socket_path=SUPERVISORD_ADDRESS_UNIX_SOCKET
    ):
        self.address = address
        self.socket_path = socket_path
        self.server = client.ServerProxy(
            self.address,
            transport=UnixStreamTransport(self.socket_path)
        )

    def start(self, process):
        try:
            self.server.supervisor.startProcess(process)
        except client.Fault as fault:
            if fault.faultCode != SupervisordProcessStates.ALREADY_STARTED:
                raise fault

    def stop(self, process_name: str):
        try:
            self.server.supervisor.stopProcess(process_name)
        except client.Fault as fault:
            if fault.faultCode != SupervisordProcessStates.NOT_RUNNING:
                raise fault

    def restart(self, process_name: str):
        process = self.process_info(process_name)

        self.stop(process.name)
        self.start(process.name)

    def view_logs(self, process):
        ...

    def version(self) -> str:
        return self.server.supervisor.getVersion()

    def process_info(self, process_name) -> ProcessInfo:
        process = self.server.supervisor.getProcessInfo(process_name)

        if not process:
            RuntimeError('process not found')

        return ProcessInfo(**process)

    def all_process_info(self) -> typing.List[ProcessInfo]:
        process_info = []

        for process in self.server.supervisor.getAllProcessInfo():
            process_info.append(ProcessInfo(**process))

        return process_info

    def reload_config(self) -> None:
        self.server.supervisor.reloadConfig()
