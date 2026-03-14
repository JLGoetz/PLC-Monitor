from django.shortcuts import render
from django.core.cache import cache

def dashboard(request):
    data = cache.get('plc_live_state', {})

    #Have to clean the data from the PLC:
    data_to_send= {}
    for name, infor in data.items():
        clean_values = {
            'sys_on': info['values'].get('Program:MainProgram.SysOn'),
            'v1_extended': info['values'].get('Program:MainProgram.Valve1_.Extended'),
        }
        data_to_send[name] = {
            'status': info['status'],
            'values': clean_values,
        }

    return render(request, 'monitor_app/dashboard.html', {'plc_data': data_to_send})
# Create your views here.
