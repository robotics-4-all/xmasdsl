import os
from os.path import join
from textx import language, metamodel_from_file, get_children_of_type, TextXSemanticError
import pathlib
import textx.scoping.providers as scoping_providers
from rich import print, pretty
from textx.scoping import ModelRepository, GlobalModelRepository
from xmasdsl.definitions import MODEL_REPO_PATH
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

pretty.install()

CURRENT_FPATH = pathlib.Path(__file__).parent.resolve()

GLOBAL_REPO = GlobalModelRepository()


def get_metamodel(debug=False) -> Any:
    metamodel = metamodel_from_file(
        CURRENT_FPATH.joinpath('grammar/xmas.tx'),
        auto_init_attributes=True,
        # global_repository=GLOBAL_REPO,
        debug=debug
    )

    metamodel.register_scope_providers(
        {
            "*.*": scoping_providers.FQNImportURI(importAs=True),
        }
    )
    return metamodel


def build_model(model_path: str, debug: bool = False):
    # Parse model
    mm = get_metamodel(debug=debug)
    model = mm.model_from_file(model_path)
    return model


def validate_model_file(model_path: str):
    _model = build_model(model_path)


def get_model_grammar(model_path):
    mm = get_metamodel()
    grammar_model = mm.grammar_model_from_file(model_path)
    return grammar_model


@language('xmas', '*.xmas')
def xmas_language():
    "ISSEL Xmas DSL"
    mm = get_metamodel()
    return mm