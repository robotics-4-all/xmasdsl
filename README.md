
![ScreenShot](/images/logo.png)

# Description
A textual DSL that allows manipulation of a led strip, placed on a wall or Christmass tree! The available commands and examples can be seen below:

# Data types

## 1. Color
```
Color MyColor [RedValue , GreenValue, BlueValue]  // values from 0 to 255
```
Example:
```
Color Blue [0, 0, 255]
```

## 2. Range
```
Range MyRange [startIndex : stopIndex : increment]  
```
Example:
```
Range BottomHalf [0:140:1]
```

## 3. RandomRange // TODO

# Blocks
## 1. Serial
```
Color MyColor [RedValue , GreenValue, BlueValue]  // values from 0 to 255
```
Example:
```
Color Blue [0, 0, 255]
```

## 2. Parallel
```
Range MyRange [startIndex : stopIndex : increment]  
```
Example:
```
Range BottomHalf [0:140:1]
```

## 3. Group // TODO

## 4. Program // TODO

## 5. Repeat // TODO

# Installation

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


# Run the API server

```bash
API_KEY=123 uvicorn xmasdsl.api:api --host 0.0.0.0 --port 8090 --reload
```

The API_KEY environmental variable has an obvious purpose!


# Use the CLI

```bash
venv [I] ➜ xmas --help
Usage: xmasdsl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  gen       M2T transformation
  validate  Model Validation

```
