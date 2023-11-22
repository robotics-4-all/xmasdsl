import os
from os.path import join
from rich import print, pretty
from xmasdsl.definitions import MODEL_REPO_PATH
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

pretty.install()


def transform(model) -> Dict[str, Any]:
    print(model)
    xmas_json: Dict[str, Any] = {
        'Eurichon': 'Transform me please :)'
    }
    ## TODO: Implement the M2T here!!
    return xmas_json
