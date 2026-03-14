from django.core.management.base import BaseCommand
from monitor_app.plc_worker import PLCWatcher, PLC_MAP

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Starting persistent PLC worker...")
        watcher = PLCWatcher(PLC_MAP)
        watcher.run()