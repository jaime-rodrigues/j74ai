metadata = {
    "name": "orchestrator_ping",
    "description": "Simple ping skill to test orchestrator runtime availability.",
    "args": {}
}

def execute(**kwargs):
    return {"status": "pong", "source": "orchestrator"}
