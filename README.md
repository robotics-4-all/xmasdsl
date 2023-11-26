# xmasdsl
XmasDSL

## Installation

We suggest you create a Python venv.

```bash
python -m venv venv && source ./venv/bin/activate
```
or for windows
```
source ./venv/Scripts/activate
```

Install the DSL in development mode to track changes automatically:

```bash
python setup.py develop
```


## Run the API server

```bash
API_KEY=123 uvicorn xmasdsl.api:api --host 0.0.0.0 --port 8090 --reload
```

The API_KEY environmental variable has an obvious purpose!


## Use the CLI

```bash
venv [I] ➜ xmas --help
Usage: xmasdsl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  gen       M2T transformation
  validate  Model Validation

```
