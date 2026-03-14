import time
from pycomm3 import LogixDriver
from django.core.cache import cache

class PLCWatcher:
    def __init__(self, config):
        self.config = config
        self.running = True

    def run(self):
        drivers = {name: LogixDriver(cfg['ip']) for name, cfg in self.config.items()}
        
        while self.running:
            state = {}
            for name, drive in drivers.items():
                try:
                    if not drive.connected: drive.open()
                    values = drive.read(*self.config[name]['tags'])
                    state[name] = {'values': {t.tag: t.value for t in values}, 'status': 'Online'}
                except Exception as e:
                    state[name] = {'status': 'Offline', 'error': str(e)}
                    if drive.connected: drive.close()
            
            cache.set('plc_live_state', state)
            time.sleep(0.5) # Poll every 500ms

PLC_MAP = {
    'PLC_1': {'ip': '10.22.128.92', 'tags': ['Program:MainProgram.Sys_On', 'Program:MainProgram.Valve1_.Extended_LS']},
    'PLC_2': {'ip': '10.22.129.112', 'tags': ['Program:MainProgram.Sys_On', 'Program:MainProgram.Valve1_.Extended_LS']},
}