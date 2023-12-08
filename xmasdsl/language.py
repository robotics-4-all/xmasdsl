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
    # raise_validation_error(
    #     LANDUAGE_COMPONENT,
    #     f'Board {c.board.name} does not have a pin '
    #     f'named {pin_conn.boardPin}'
    # )
def entity_obj_processor(entity):
	'''
	Check that Ethe ntity names are capitalized. This could also be specified
	in the grammar using regex match but we will do that check here just
	as an example.
	'''
	# print(entity.name)
	pass
#   if entity.name != entity.name.capitalize():
#     raise TextXSemanticError('Entity name "%s" must be capitalized.' %
#                             entity.name, **get_location(entity))
    
def attribute_obj_processor(attribute):
	print("Attribute Proccessor!!")
	'''
	Obj. processors can also introduce changes in the objects they process.
	Here we set "primitive" attribute based on the Entity they refer to.
	'''
	# attribute.primitive = attribute.type.name in ['integer', 'string']	
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
        # EMPTY
        'Entity': entity_obj_processor,
    	'Attribute': attribute_obj_processor,
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
