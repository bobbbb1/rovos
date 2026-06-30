# src/example/launch/example.launch.py

def generate_launch_description():
    return {
        "nodes": [
            {
                "package": "example",
                "node": "talker.py",
                "config": False
            },
            {
                "package": "example",
                "node": "talk_config.py",
                "config": "config.yaml"
            },
            {
                "package": "example",
                "node": "listen.py"
            }
        ]
    }