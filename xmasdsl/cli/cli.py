import click
import os
from rich import print, pretty
import json

from xmasdsl.language import build_model
from xmasdsl.m2t import model_to_json

pretty.install()

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command('validate', help='Model Validation')
@click.pass_context
@click.argument('model_path')
def validate(ctx, model_path):
    model = build_model(model_path)
    print('[*] Model validation success!!')


@cli.command('gen', help='M2T transformation')
@click.pass_context
@click.argument('model_path')
def generate(ctx, model_path):
    model = build_model(model_path)
    model_json = model_to_json(model)
    filepath = f'xmas.json'
    with open(filepath, 'w') as fp:
        json.dump(model_json, fp)


def main():
    cli(prog_name='xmasdsl')
