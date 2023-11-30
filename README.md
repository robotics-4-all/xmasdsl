
![ScreenShot](https://media.discordapp.net/attachments/1176508348372369408/1176510791151796404/Screenshot_2023-11-21_at_15.13.45.png)

# Description
A textual DSL that allows manipulation of a led strip, placed on a wall or Christmass tree! The available commands and examples can be seen below:

# Data types

## 1. Color
```
Color MyColor [RedValue, GreenValue, BlueValue]  // values from 0 to 255
```
<b>Example:</b>
```
Color Blue [0, 0, 255]
```

## 2. Range
```
Range MyRange [startIndex : stopIndex : increment]  
```
<b>Example:</b>
```
Range BottomHalf [0:140:1]
```

## 3. RandomRange // TODO

# Blocks

## 1. Program
This is the most outer block. All other blocks (apart from [Group](/#Group)) exist inside this one. Each block opens with ```{``` and ends with ```}```  
<b>Example:</b>
```
Program {
  ...other blocks
}
```

## 2. Serial
All the commands in the block will execute one after the other.  
<b>Example:</b>
```
Program {
	Serial {
  		...other blocks
	}
}
```

Note: by default the Program block executes the inside blocks serially.

## 3. Parallel
All the commands in the block will execute one after the other.  
<b>Example:</b>
```
Program {
	Serial {
  		...other blocks
	}
}
```


## 4. Group // TODO

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
