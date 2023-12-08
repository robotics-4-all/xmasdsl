import os
import json
from os.path import join
from rich import print, pretty
from xmasdsl.definitions import MODEL_REPO_PATH
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

pretty.install()

MAX_PERCENTAGE = 100


def _is(object):
    return object.__class__.__name__


def _has(object, key):
    return (key in object.__dict__.keys())


def _parseChangedBy(object):
    if object.changeBy:
        return f"{object.changeBy}{object.val}"

    return object.val


def _parseArgument(object):
    if object.color != None:
        return [
            str(_parseChangedBy(object.color.r)),
            str(_parseChangedBy(object.color.g)),
            str(_parseChangedBy(object.color.b))
        ]
    elif object.colorDef != None:
        return [
            str(_parseChangedBy(object.colorDef.color.r)),
            str(_parseChangedBy(object.colorDef.color.g)),
            str(_parseChangedBy(object.colorDef.color.b))
        ]


def _parseColor(object):
    if object.colorDef != None and _has(object.colorDef, "colorA") and _has(object.colorDef, "colorB"):
        return {
            "colorA": _parseArgument(object.colorDef.colorA),
            "colorB": _parseArgument(object.colorDef.colorB)
        }

    else:
        return {
            "colorA": _parseArgument(object),
            "colorB": []
        }


def _parseRange(object):
    if object.hasEnd == ":" and object.hasStep == ":":
        return f"{object.start}:{object.end}:{_parseChangedBy(object.step)}"
    elif object.hasEnd == ":" and object.hasStep != ":":
        return f"{object.start}:{object.end}"
    else:
        return f"{object.start}"


def _parseRanges(object):
    pixels = None
    percentage = 100

    if object.range != None:
        pixels = ",".join([_parseRange(r) for r in object.range.ranges])
    elif _has(object.rangeDef, "percentage"):
        pixels = _parseRange(object.rangeDef.range)
        percentage = object.rangeDef.percentage
    else:
        pixels = ",".join([_parseRange(r)
                          for r in object.rangeDef.range.ranges])

    return {
        "pixels": pixels,
        "percentage": min(percentage, MAX_PERCENTAGE)
    }


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
                "range": _parseRanges(model.range),
                "color": _parseColor(model.color),
                "duration": model.duration,
                "maintain": model.maintain
            }
        }
    elif _is(model) == "Dim":
        return {
            "dim": {
                "range": _parseRanges(model.range),
                "color": _parseColor(model.color),
                "duration": model.duration,
                "fadeIn": model.fadeIn
            }
        }
    elif _is(model) == "Rainbow":
        return {
            "rainbow": {
                "range": _parseRanges(model.range),
                "colorStart": _parseColor(model.colorStart),
                "colorEnd": _parseColor(model.colorEnd),
                "duration": model.duration,
                "maintain": model.maintain
            }
        }

    elif _is(model) == "Linear":
        return {
            "linear": {
                "rangeStart": _parseRanges(model.rangeStart),
                "rangeEnd": _parseRanges(model.rangeEnd),
                "colorStart": _parseColor(model.colorStart),
                "colorEnd": _parseColor(model.colorEnd),
                "duration": model.duration,
                "maintain": model.maintain
            }
        }
    else:
        pass


def transform(model) -> Dict[str, Any]:
    json_model = objectToJSON(model.program)

    print(json_model)

    xmas_json: Dict[str, str] = json.dumps({
        'program': json_model
    })

    return xmas_json
