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
from textx import get_location, TextXSemanticError

MAX_LEDS = 449

pretty.install()

CURRENT_FPATH = pathlib.Path(__file__).parent.resolve()

GLOBAL_REPO = GlobalModelRepository()

def raise_validation_error(obj, msg):
    raise TextXSemanticError(
        f'[Validation Error]: {msg}',
        **get_location(obj)
    )

def model_proc(model, metamodel):
    pass

def color_obj_processor(color):
	# print("Color:", color)
	if int(color.r.val) > 255 or int(color.r.val) < 0:
		raise_validation_error(color, "Red value out of range: [0, 255]")
	if int(color.g.val) > 255 or int(color.g.val) < 0:
		raise_validation_error(color, "Green value out of range: [0, 255]")
	if int(color.b.val) > 255 or int(color.b.val) < 0:
		raise_validation_error(color, "Blue value out of range: [0, 255]")

# def random_color_obj_processor(rand_color):
#     # print("Random color:", rand_color.__dict__)
#     if rand_color.color != None:
#         # print("---", rand_color.color.__dict__)
#         color_obj_processor(rand_color.color)
#     pass

def range_obj_processor(range):
	# print("Range:", range.__dict__)
	if int(range.start) < 0 or int(range.end) > MAX_LEDS or int(range.start) > MAX_LEDS:
		raise_validation_error(range, f'Invalid range. Value is out of bounds: [0, {MAX_LEDS}]')
	pass

def random_range_obj_processor(rand_range):
    # print("Rand_range", rand_range.__dict__)
    if (int(rand_range.percentage) > 100 or int(rand_range.percentage) < 0):
        raise_validation_error(rand_range, f'Invalid percentage. Value is out of bounds: [0, 100]')
    pass

def linear_obj_processor(linear):
    # print("Linear", linear)
    pass
  
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
            "*.*": scoping_providers.FQN(),
        }
    )
    metamodel.register_model_processor(model_proc)

    metamodel.register_obj_processors({
        # 'RandomColorArgument': random_color_obj_processor,
        'Color': color_obj_processor,
        'Range': range_obj_processor,
        'RandomRangeDef': random_range_obj_processor,
        'Linear': linear_obj_processor,
    })
    
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
