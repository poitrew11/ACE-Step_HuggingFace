import requests
import time
import vast_api

TARGET_LOAD = 70  # %
MAX_WORKERS = 10
MIN_WORKERS = 1

def get_current_load():
    resp = requests.get("http://<NGINX_IP>/metrics")
    return resp.json()["load_percent"]

def adjust_workers():
    load = get_current_load()
    current_workers = vast_api.get_running_workers()
    
    if load > TARGET_LOAD and current_workers < MAX_WORKERS:
        vast_api.create_instance()  # +1 worker
    elif load < TARGET_LOAD and current_workers > MIN_WORKERS:
        vast_api.terminate_oldest_worker()  # -1 worker

while True:
    adjust_workers()
    time.sleep(60)
