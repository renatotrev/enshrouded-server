import os, hmac
import functions_framework
from google.cloud import compute_v1

PROJECT = os.environ["PROJECT"]
TOKEN = os.environ["TOKEN"]
ZONE, NAME = "us-east1-c", "enshrouded"
client = compute_v1.InstancesClient()

@functions_framework.http
def vm(request):
    key = request.args.get("key", "")
    if not hmac.compare_digest(key, TOKEN):
        return ("Forbidden", 403)

    action = request.args.get("action", "status")
    inst = client.get(project=PROJECT, zone=ZONE, instance=NAME)

    if action == "start" and inst.status in ("TERMINATED", "STOPPED"):
        client.start(project=PROJECT, zone=ZONE, instance=NAME)
        return "Starting... wait about 2-3 minutes before joining."
    if action == "stop" and inst.status == "RUNNING":
        client.stop(project=PROJECT, zone=ZONE, instance=NAME)
        return "Stopping."
    return f"Server status: {inst.status}"
