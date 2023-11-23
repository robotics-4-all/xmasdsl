import os
import json
from os.path import join
from rich import print, pretty
from xmasdsl.definitions import MODEL_REPO_PATH
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

pretty.install()


def _is(object):
    return object.__class__.__name__


def _parseChangedBy(object):
    if object.changeBy:
        return f"{object.changeBy}{object.val}"

    return object.val


def _parseColor(object):
    return [
        str(_parseChangedBy(object.color.r)),
        str(_parseChangedBy(object.color.g)),
        str(_parseChangedBy(object.color.b))
    ]


def _parseRange(object):
    if object.hasEnd == ":" and object.hasStep == ":":
        return f"{object.start}:{object.end}:{_parseChangedBy(object.step)}"
    elif object.hasEnd == ":" and object.hasStep != ":":
        return f"{object.start}:{object.end}"
    else:
        return f"{object.start}"


def _parsePixels(object):
    return ",".join([_parseRange(r) for r in object.range.ranges])


def objectToJSON(model):
    if _is(model) == "Serial" or _is(model) == "Program":
        serial_commands = []

        for cmd in model.commands:
            serial_commands.append(objectToJSON(cmd))

        return {"serialProcess": serial_commands}

    elif _is(model) == "Parallel":
        parallel_processes = []

        for cmd in model.processes:
            parallel_processes.append(objectToJSON(cmd))

        return {"parallelProcess": parallel_processes}

    elif _is(model) == "Repeat":
        serial_repeat = []

        for cmd in model.commands:
            serial_repeat.append(objectToJSON(cmd))

        return {"repeat": {"times": model.times, "serialProcess": serial_repeat}}

    elif _is(model) == "GroupRef":
        group_commands = []

        for cmd in model.ref.commands:
            group_commands.append(objectToJSON(cmd))

        return {"serialProcess": group_commands}

    elif _is(model) == "SetBrightness":
        return {
            "setBrightness": {
                "value": _parseChangedBy(model.value)
            }
        }

    elif _is(model) == "Delay":
        return {
            "delay": {
                "duration": _parseChangedBy(model.duration)
            }
        }
    elif _is(model) == "SetPixelColor":
        return {
            "setPixelColor": {
                "pixels": _parsePixels(model.pixels),
                "color": _parseColor(model.color),
                "duration": model.duration
            }
        }
    else:
        pass


def transform(model) -> Dict[str, Any]:
    json_model = objectToJSON(model.program)

    xmas_json: Dict[str, str] = json.dumps({
        'program': json_model
    })

    return xmas_json
