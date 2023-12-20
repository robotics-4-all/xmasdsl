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
        total_duration = 0
        serial_commands = []
        for cmd in model.commands:
            sub_json, sub_duration = objectToJSON(cmd)

            serial_commands.append(sub_json)
            total_duration += sub_duration

        return {"serialProcess": serial_commands}, total_duration

    elif _is(model) == "Parallel":
        parallel_durations = []
        parallel_processes = []

        for cmd in model.processes:
            sub_json, sub_duration = objectToJSON(cmd)

            parallel_processes.append(sub_json)
            parallel_durations.append(sub_duration)

        return {"parallelProcess": parallel_processes}, max(parallel_durations)

    elif _is(model) == "Repeat":
        total_duration = 0
        serial_repeat = []

        for cmd in model.commands:
            sub_json, sub_duration = objectToJSON(cmd)

            serial_repeat.append(sub_json)
            total_duration += sub_duration

        return {"repeat": {"times": model.times, "serialProcess": serial_repeat}}, (total_duration * int(model.times))

    elif _is(model) == "GroupRef":
        total_duration = 0
        group_commands = []

        for cmd in model.ref.commands:
            sub_json, sub_duration = objectToJSON(cmd)

            group_commands.append(sub_json)
            total_duration += sub_duration

        return {"serialProcess": group_commands}, total_duration

    elif _is(model) == "SetBrightness":
        return {
            "setBrightness": {
                "value": _parseChangedBy(model.value)
            }
        }, 0
    elif _is(model) == "Delay":
        return {
            "delay": {
                "duration": _parseChangedBy(model.duration)
            }
        }, int(model.duration.val)

    elif _is(model) == "SetPixelColor":
        return {
            "setPixelColor": {
                "range": _parseRanges(model.range),
                "color": _parseColor(model.color),
                "duration": model.duration,
                "maintain": model.maintain
            }
        }, int(model.duration)

    elif _is(model) == "Dim":
        return {
            "dim": {
                "range": _parseRanges(model.range),
                "color": _parseColor(model.color),
                "duration": model.duration,
                "fadeIn": model.fadeIn
            }
        }, int(model.duration)

    elif _is(model) == "Rainbow":
        return {
            "rainbow": {
                "range": _parseRanges(model.range),
                "colorStart": _parseColor(model.colorStart),
                "colorEnd": _parseColor(model.colorEnd),
                "duration": model.duration,
                "maintain": model.maintain
            }
        }, int(model.duration)

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
        }, int(model.duration)
    else:
        return {}, 0


def transform(model) -> Dict[str, Any]:
    json_model, duration = objectToJSON(model.program)

    print("Total duration is:", duration)

    xmas_json: Dict[str, str] = json.dumps({
        'program': json_model,
        'duration': duration
    })

    return xmas_json
