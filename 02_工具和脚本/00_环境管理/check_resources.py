import platform
import psutil
import json

info = {
    'os': {
        'system': platform.system(),
        'release': platform.release(),
        'machine': platform.machine()
    },
    'cpu': {
        'physical_cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(logical=True)
    },
    'memory': {
        'total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        'available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
        'percent_used': psutil.virtual_memory().percent
    },
    'disk': {
        'total_gb': round(psutil.disk_usage('.').total / (1024**3), 2),
        'available_gb': round(psutil.disk_usage('.').free / (1024**3), 2),
        'percent_used': psutil.disk_usage('.').percent
    }
}

print(json.dumps(info, indent=2, ensure_ascii=False))