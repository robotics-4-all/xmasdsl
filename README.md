
![ScreenShot](https://media.discordapp.net/attachments/1176508348372369408/1176510791151796404/Screenshot_2023-11-21_at_15.13.45.png)

## Description
A textual DSL that allows manipulation of a led strip, placed on a wall or Christmass tree! The available commands and examples can be seen below:

## Data types

### 1. Color
```
Color MyColor [RedValue, GreenValue, BlueValue]  // values from 0 to 255
```
<b>Example:</b>
```
Color Blue [0, 0, 255]
```

### 2. Range
```
Range MyRange [startIndex : stopIndex : increment]  
```
<b>Example:</b>
```
Range BottomHalf [0:140:1]
```

### 3. RandomRange // TODO

## Blocks

### 1. Program
This is the most outer block. All other blocks (apart from [Group](/#Group)) exist inside this one. Each block opens with ```{``` and ends with ```}```  
<b>Example:</b>
```
Program {
  ...other blocks or commands
}
```

### 2. Serial
All the commands in the block will execute one after the other.  
<b>Example:</b>
```
Program {
	Serial {
  		...other blocks or commands
	}
}
```

Note: by default the Program block executes the inside blocks serially.

### 3. Parallel
This one is meant for blocks and not commands. All the blocks inside will be executed in concurrently. For example you can light up the topHalf of the led strip int blue and the bottom half in red.  
<b>Example:</b>
```
Program {
	Parallel {
		Serial {
			Command1
		}
		Serial {
			Command2
		}
  		...other blocks
	}
}
```

### 4. Group
Use this block to create reusable actions. The actions are referenced by their name inside other blocks.  
<b>Example:</b>
```
Group LightBottom {
	...other blocks or commands
}

Group LightTop {
	...other blocks or commands
}

Program {
	LightBottom
	LightTop
}
```

### 5. Repeat 
Use this block to run the commands (or blocks) inside many times.
```
Repeat NUM_OF_TIMES {
	...other blocks or commands
}
```
<b>Example:</b>
```
Group LightBottom {
	...other blocks or commands
}

Group LightTop {
	...other blocks or commands
}

Group TurnOFF {
	...other blocks or commands
}

Program {
	Repeat 10 {
		LightBottom
		LightTop
		TurnOFF
	}
}
```

## Commands

### 1. SetPixelColor
```
SetPixelColor(RANGE, COLOR, DURATION, MAINTAIN=true)
```

### 2. Dim
```
Dim(RANGE, COLOR, DURATION, FADE_IN=false)
```

### 3. Rainbow
```
Rainbow(RANGE, START_COLOR, END_COLOR, DURATION, MAINTAIN=false)
```

### 4. Linear
```
Linear(START_RANGE, END_RANGE, START_COLOR, END_COLOR, DURATION, MAINTAIN=false)
```

### 5. Delay
```
Delay(DURATION)
```

## Examples

### 1. Color rotation
```
Range Part1 [1:90:1]
Range Part2 [90:180:1]
Range Part3 [180:270:1]
Color Green [0, 240, 0]
Color Red [255, 0, 0]
Color Blue [0, 0, 255]

Group Light1 {
  Parallel {
    Serial{
      SetPixelColor(Part1, Red, 200)
    }
    Serial{
      SetPixelColor(Part2, Blue, 200)
    }
    Serial{
      SetPixelColor(Part3, Green, 200)
    }
  }
}

Group Light2 {
  Parallel {
    Serial{
      SetPixelColor(Part1, Green, 200)
    }
    Serial{
      SetPixelColor(Part2, Red, 200)
    }
    Serial{
      SetPixelColor(Part3, Blue, 200)
    }
  }
}

Group Light3 {
  Parallel {
    Serial{
      SetPixelColor(Part1, Blue, 200)
    }
    Serial{
      SetPixelColor(Part2, Green, 200)
    }
    Serial{
      SetPixelColor(Part3, Red, 200)
    }
  }
}

Program {
  Repeat 3000 {
    Light1
    Light2
    Light3
  }
}
```

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
