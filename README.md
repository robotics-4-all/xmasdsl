![ScreenShot](https://media.discordapp.net/attachments/1176508348372369408/1176510791151796404/Screenshot_2023-11-21_at_15.13.45.png)

## Description

A textual DSL that allows manipulation of a led strip, placed on a wall or Christmass tree! The available commands and examples can be seen below:

XmasDSL posses various <b>Data Types</b> for pixel and color manipulation, <b>Functions</b> that implement specific animations as well as <b>Structural Components</b> that manipulate the program flow.

## Data types

### Color

In XmasDSL currently there are three ways that one can select a color.

#### 1. Direct Color Replacement

Place the color component directly inside a function.

```
Function (..., [RedValue, GreenValue, BlueValue], ...) // each value can range from 0 to 255
```

<b>Example:</b>

```
SetPixelColor(Pixels, [255, 0, 0], duration, maintain)
```

#### 2. Color Declaration

Declare a color component that from now own it will be referred with a name.

```
Color MyColor [RedValue, GreenValue, BlueValue] // Each value can range from 0 to 255
```

<b>Example:</b>

```
Color Red [255, 0, 0]       // This creates a red Color
Color Green [0, 0, 255]     // This creates a green Color
Color Blue [0, 0, 255]      // This creates a blue Color
```

#### 3. Random Color Declaration

Declare a color component that will receive a random color between two values. These values can be a direct color replacement or a color declaration.

```
RandomColor myRandColor ([RedValue, GreenValue, BlueValue], AnotherColorDeclaration)
```

<b>Example:</b>

```
Color Red [255, 0, 0]
RandomColor myRandColor ([0, 255, 0], Red) // This will generate a random color between the colors blue & red
```

```
Note: A random Color declaration cannot be used inside another random Color declaration.
```

### Range

Ranges are practically groups of pixels. All functions in order to work properly require at least one pixel group and one color. A Range can contain one or more group of Pixels, separated by a comma. A group can be a single Value or a continue series of pixels.

```
[startingPixel]                     // a single pixel.
[startingPixel:endingPixel]         // all pixels from startingPixel to endingPixel.
[startingPixel:endingPixel:step]    // all pixels from startingPixel to endingPixel moving by step pixels.
```

#### 1. Direct Range Replacement

Place the Range type directly inside a function.

```
Function ([pixel1, pixel2, pixel3], Red, ...)           // this range reference the pixel1, pixel2, pixel3 of the led strip.
Function ([startingPixel:endingPixel], Red, ...)        // this range reference all the pixels from the 1st till the 10th (including it).
Function ([startingPixel:endingPixel:step], Red, ...)   // this range reference all the even pixels between the 1st and the 10th (including it).
```

<b>Example:</b>

```
SetPixelColor([2, 7, 10], Red, duration, maintain)      // this reference pixels [2, 7, 10] of the led strip.
SetPixelColor([1:10], Red, duration, maintain)          // this reference pixels [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] of the led strip.
SetPixelColor([0:10:2], Red, duration, maintain)        // this reference pixels [0, 2, 4, 6, 8, 10] of the led strip.
SetPixelColor([1:10:2, 15], Red, duration, maintain)    // this reference pixels [1, 3, 5, 7, 9, 15] of the led strip.
```

#### 2. Range Declaration

Declare a Range of pixels component that from now own it will be referred with a name.

```
Range myRange1 [pixel1, pixel2, pixel3]                 // this range reference the pixel1, pixel2, pixel3 of the led strip.
Range myRange2 [startingPixel:endingPixel]              // this range reference all the pixels from the 1st till the 10th (including it).
Range myRange3 [startingPixel:endingPixel:step]         // this range reference all the even pixels between the 1st and the 10th (including it).
```

<b>Example:</b>

```
Range myRange1 [2, 7, 10]                               // this reference pixels [2, 7, 10] of the led strip.
Range myRange2 [1:10]                                   // this reference pixels [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] of the led strip.
Range myRange3 [0:10:2]                                 // this reference pixels [0, 2, 4, 6, 8, 10] of the led strip.
Range myRange4 [1:10:2, 15]                             // this reference pixels [1, 3, 5, 7, 9, 15] of the led strip.
```

#### 3. Random Range Declaration

Declare a Random Range of pixels. This Random Range will be constituted by randomly selected pixels from teh original Range with a [x]% chance.

```
Range myRandomRange1 ([pixel1, pixel2, pixel3], 30)     // this range reference the pixel1, pixel2, pixel3 of the led strip.
Range myRandomRange2 ([startingPixel:endingPixel], 50)  // this range reference all the pixels from the 1st till the 10th (including it).
```

<b>Example:</b>

```
Range myRandomRange1 ([2, 7, 10], 30)                   // this random Range selects 30% of pixel Range [2, 7, 10].
Range myRandomRange2 ([1:10], 10)                       // this random Range selects 30% of pixel Range [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

```
Note: A random Range declaration cannot be used inside another random Range declaration.
```

## Blocks

### 1. Program

This is the most outer block. All other blocks (apart from [Group](/#Group)) exist inside this one. Each block opens with `{` and ends with `}`  
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

This function sets the color of a specified pixel range for a given time DURATION(milliseconds). If MAINTAIN is set to `true`, the pixels will retain their color until changed again. MAINTAIN defaults to `true`.

```
SetPixelColor(RANGE, COLOR, DURATION, MAINTAIN=true)
```

<b>Examples:</b>

```
SetPixelColor(Top, Red, 1000) // where Top is a pixel range defined
							  // earlier and Red is a defined Color
SetPixelColor([1:10:1], [255, 255, 0], 1000)
SetPixelColor([1:10:1], [255, 255, 0], 1000, True)
```

### 2. Dim

This function fades in or fades out (according the the boolean parameter FADE_IN) the pixels of RANGE. The animation speed will depend on the chosen DURATION(milliseconds). FADE_IN defaults to false.

```
Dim(RANGE, COLOR, DURATION, FADE_IN=false)
```

<b>Examples:</b>

```
Dim([1:100:1], Red, 1000, true)
Dim(Top, [100, 100, 100], 1000)
```

### 3. Rainbow

This function tansitions the color of the given pixel range from START_COLOR to END_COLOR in the specified DURATION(milliseconds). If MAINTAIN is set to `true`, the pixels will retain their color until changed again. MAINTAIN defaults to `false`.

```
Rainbow(RANGE, START_COLOR, END_COLOR, DURATION, MAINTAIN=false)
```

<b>Examples:</b>

```
Rainbow(Top, [255, 0, 0], [0, 255, 0], 1000)
Rainbow([1:100:1], Red, Blue, 1000, False)
```

### 4. Linear

This function "moves" the pixel range defined in START_RANGE to the END_RANGE. It will traverse the pixels in between until it reaches the end. At the same time, it will transition the colors of the pixels from START_COLOR to END_COLOR. If MAINTAIN is set to `true`, the pixels will retain their color until changed again. MAINTAIN defaults to `false`.

```
Linear(START_RANGE, END_RANGE, START_COLOR, END_COLOR, DURATION, MAINTAIN=false)
```

<b>Examples:</b>

```
Linear(Top, Bot, Red, Blue, 1000)
Linear([1:100:1], [1:100:1], Red, Blue, 1000, True)
Linear(Top, Bot, [100, 100, 100], Blue, 1000, False)
```

### 5. Delay

This function will stop the flow of the execution for the specified time in milliseconds.

```
Delay(DURATION)
```

<b>Example:</b>

```
Delay(500)
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
