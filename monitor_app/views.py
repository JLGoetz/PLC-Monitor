from django.shortcuts import render
from django.core.cache import cache

def dashboard(request):
    data = cache.get('plc_live_state', {})
    return render(request, 'dashboard.html', {'plc_data': data})