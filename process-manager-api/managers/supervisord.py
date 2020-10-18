import socket
import subprocess
from http.client import HTTPConnection
from pathlib import Path
from typing import List
from xmlrpc import client

import managers
from managers import ProcessModel


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


class Supervisord(managers.ProcessManagerProtocol):
    def __init__(
            self,
            address='http://localhost',
            socket_path='/var/run/supervisor/supervisor.sock'
    ):
        self.address = address
        self.socket_path = socket_path
        self.server = client.ServerProxy(
            self.address,
            transport=UnixStreamTransport(self.socket_path)
        )

    def _list_methods(self):
        return self.server.system.listMethods()

    def reload_daemon(self):
        try:
            subprocess.call(['supervisorctl', 'reload_daemon'])
        except subprocess.CalledProcessError as ignored:
            pass

    def status(self, process):
        return self.server.supervisor.getProcessInfo(process)

    def start(self, process):
        try:
            self.server.supervisor.startProcess(process)
        except client.Fault as fault:
            if fault.faultCode != 60:  # ALREADY STARTED
                raise fault

    def stop(self, process):
        try:
            self.server.supervisor.stopProcess(process)
        except client.Fault as fault:
            if fault.faultCode != 70:  # NOT RUNNING
                raise fault

    def restart(self, process):
        self.stop(process)
        self.start(process)

    def __get_unit_files(self, abspath_supervisor='/etc/supervisord.d/') -> List[Path]:
        path = Path(abspath_supervisor)
        return list(path.glob('*.ini')) + list(path.glob('*.conf')) + list(path.glob('*.off'))

    def enable(self, unit):
        _unit_file = list(filter(lambda v: v.name == unit, self.__get_unit_files()))

        if len(_unit_file) <= 0:
            raise RuntimeError('unit "{}" not exist'.format(unit))
        else:
            unit_file = _unit_file[0]
            if unit_file.stem.endswith('off'):
                unit_file.rename(unit_file.with_suffix(''))
            else:
                raise RuntimeWarning('unit "{}" already enable'.format(unit))

    def disable(self, unit):
        _unit_file = list(filter(lambda v: v.name == unit, self.__get_unit_files()))

        if len(_unit_file) <= 0:
            raise RuntimeError('unit "{}" not exist'.format(unit))
        else:
            unit_file = _unit_file[0]
            if unit_file.stem.endswith('off'):
                unit_file.rename(unit_file.name + '.off')
            else:
                raise RuntimeWarning('unit "{}" already disable'.format(unit))

    def view_logs(self, process: ProcessModel):
        pass

    @property
    def units(self):
        units_id = []
        for unit in self.__get_unit_files():
            units_id.append(unit.stem)

        return units_id

    @property
    def version(self):
        return self.server.supervisor.getVersion()

    @property
    def process(self):
        units_complete_info = self.server.supervisor.getAllProcessInfo()
        units_names = []

        for unit in units_complete_info:
            units_names.append(unit['name'])

        return units_names
