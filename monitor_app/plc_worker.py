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
    'PLC_1': {'ip': '192.168.1.10', 'tags': ['Relay_1', 'Relay_2']},
    'PLC_2': {'ip': '192.168.1.11', 'tags': ['Relay_1', 'Relay_2']},
}