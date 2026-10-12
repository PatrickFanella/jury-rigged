"""Render a disposable staging stack without shared Docker objects or ports."""
import json
import sys


def isolate(config):
    config.pop("name", None)
    for service in config["services"].values():
        service.pop("container_name", None)
        service.pop("ports", None)
        service.pop("restart", None)
    config["services"]["api"]["ports"] = ["127.0.0.1:0:3001"]
    for section in ("networks", "volumes"):
        for value in config.get(section, {}).values():
            value.pop("name", None)
            value.pop("external", None)
    return config


if __name__ == "__main__":
    json.dump(isolate(json.load(sys.stdin)), sys.stdout, indent=2)
    sys.stdout.write("\n")
