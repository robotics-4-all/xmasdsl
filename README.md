![ScreenShot](https://media.discordapp.net/attachments/1176508348372369408/1176510791151796404/Screenshot_2023-11-21_at_15.13.45.png)

## Description

A textual DSL that allows manipulation of a led strip, placed on a wall or Christmass tree! The available commands and examples can be seen below:

XmasDSL has various <b>`Data Types`</b> for pixel and color manipulation, <b>`Functions`</b> that implement specific animations as well as <b>`Structural Components`</b> that manipulate the program flow.

## Data types

### 1. Color

In XmasDSL currently there are three ways that one can select a color.

#### 1.1 Direct Color Replacement

Place the color component directly inside a function.

```
Function (..., [RedValue, GreenValue, BlueValue], ...) // each value can range from 0 to 255
```

<b>Example:</b>

```
SetPixelColor(Pixels, [255, 0, 0], duration, maintain)
```

#### 1.2 Color Declaration

Declare a color component that from now on it will be referenced with a name.

```
Color MyColor [RedValue, GreenValue, BlueValue] // Each value can range from 0 to 255
```

<b>Example:</b>

```
Color Red [255, 0, 0]       // This creates a red Color
Color Green [0, 0, 255]     // This creates a green Color
Color Blue [0, 0, 255]      // This creates a blue Color
```

#### 1.3 Random Color Declaration

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

### 2. Range

Ranges are practically groups of pixels. All functions in order to work properly require at least one pixel group and one color. A Range can contain one or more groups of Pixels, separated by a comma. A group can be a single Value or a continues series of pixels.

```
[startingPixel]                     // a single pixel.
[startingPixel:endingPixel]         // all pixels from startingPixel to endingPixel(including ending pixel).
[startingPixel:endingPixel:step]    // all pixels from startingPixel to endingPixel(including ending pixel) moving by step pixels.
```

#### 2.1 Direct Range Replacement

Place the ```Range``` type directly inside a function.

```
Function ([pixel1, pixel2, pixel3], Red, ...)           // this range reference the pixel1, pixel2, pixel3 of the led strip.
Function ([startingPixel:endingPixel], Red, ...)        // this range reference all the pixels from the 1st till the 10th (including it).
Function ([startingPixel:endingPixel:step], Red, ...)   // this range reference all the even pixels between the 1st and the 10th.
```

<b>Example:</b>

```
SetPixelColor([2, 7, 10], Red, duration, maintain)      // this reference pixels [2, 7, 10] of the led strip.
SetPixelColor([1:10], Red, duration, maintain)          // this reference pixels [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] of the led strip.
SetPixelColor([0:10:2], Red, duration, maintain)        // this reference pixels [0, 2, 4, 6, 8, 10] of the led strip.
SetPixelColor([1:10:2, 15], Red, duration, maintain)    // this reference pixels [1, 3, 5, 7, 9, 15] of the led strip.
```

#### 2.2 Range Declaration

Declare a Range of pixels component that from now on it will be referenced with a name.

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

#### 2.3 Random Range Declaration

Declare a Random Range of pixels. This Random Range will be constituted by randomly selected ```X%``` of the original Range.

```
Range myRandomRange1 ([pixel1, pixel2, pixel3], 30)     // this range reference the pixel1, pixel2, pixel3 of the led strip.
Range myRandomRange2 ([startingPixel:endingPixel], 50)  // this range reference all the pixels from the 1st till the 10th (including it).
```

<b>Example:</b>

```
Range myRandomRange1 ([2, 7, 10], 30)                   // this random Range selects 30% of pixel Range [2, 7, 10].
Range myRandomRange2 ([1:10], 10)                       // this random Range selects 10% of pixel Range [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

```
Note: A random Range declaration cannot be used inside another random Range declaration.
```

## Blocks

### 1. Program

This is the most outer block. All other blocks (apart from [Group](/#Group)) must exist inside this one. Each block opens with `{` and ends with `}`  
<b>Example:</b>

```
Program {
  ...other blocks or commands
}
```

```
Note: by default the Program block executes serially all the other blocks and commands inside it.
```
### 2. Serial

All the commands inside this block will be executed one after the other.  
<b>Example:</b>

```
Program {
	Serial {
  		...other blocks or commands
	}
}
```



### 3. Parallel

This one can contain only `Serial`, `Repeat` and `Group References`. All blocks inside it will be executed concurrently. For example you can light up the topHalf of the led strip in a blue `Color` and the bottom half in a red `Color`. The program will exit from the parallel block after the block with the highest duration finishes.  
<b>Example:</b>

```
Program {
	Parallel {
		Serial {
			SetPixelColor([0:225:1], [0, 0, 255], 1000)
		}
		Serial {
			SetPixelColor([226:450:1], [255, 0, 0], 2000)
		}
  		// ...other blocks
	}
}
```

`Note`: In this example the `Parallel` block will exit after 2000 milliseconds.

### 4. Group

Use this block to create reusable code segments. These code segments are referenced by their name inside other blocks.  
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

Use this block to serially run the commands (or blocks) inside it many times (`NUM_OF_TIMES`).

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
`Note`: This block will be executed `10` times.

## Commands

### 1. SetPixelColor

This function sets the color of the specified pixel range for a given time `DURATION` (milliseconds). If `MAINTAIN` is set to `true`, the pixels will retain their color until changed again. `MAINTAIN` defaults to `true`.

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

This function fades in (`FADE_IN` = true) or fades out (`FADE_IN` = false) the pixels of `RANGE` with the selected `Color`. The whole animation will last `DURATION` milliseconds. `FADE_IN` defaults to `false`. 

```
Dim(RANGE, COLOR, DURATION, FADE_IN=false)
```

<b>Examples:</b>

```
Dim([1:100:1], Red, 1000, true)
Dim(Top, [100, 100, 100], 1000)
```

### 3. Rainbow

This function tansitions the color of the given pixel `Range` from `START_COLOR` to `END_COLOR` in the specified `DURATION` (milliseconds). If `MAINTAIN` is set to `true`, the pixels will retain their color until changed again. `MAINTAIN` defaults to `false`.

```
Rainbow(RANGE, START_COLOR, END_COLOR, DURATION, MAINTAIN=false)
```

<b>Examples:</b>

```
Rainbow(Top, [255, 0, 0], [0, 255, 0], 1000)
Rainbow([1:100:1], Red, Blue, 1000, False)
```

### 4. Linear

This function "moves" the pixel `Range` defined in `START_RANGE` to the `END_RANGE`. It will traverse the pixels in between until it reaches the end. At the same time, it will transition the colors of the pixels from `START_COLOR` to `END_COLOR`. If `MAINTAIN` is set to `true`, the pixels will retain their color until changed again. `MAINTAIN` defaults to `false`.

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

This function will halt the flow of the execution in the current block for the specified `DURATION` in milliseconds.

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
Range Part1 [0:150:1]
Range Part2 [150:300:1]
Range Part3 [300:450:1]
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

### 2. Random Range

```
Color Green [0, 230, 0]
Color Red [255, 0, 0]
Color Blue [0, 0, 255]
Color Dark [5, 5, 5]

RandomRange Rand1 ([0:449:1], 30)
Range All [0:449:1]

Group TurnDark {
  SetPixelColor(All, Dark, 1, false)
}

Program {
  TurnDark
  Repeat 5 {
    SetPixelColor(Rand1, Red, 500, false)
    TurnDark
    SetPixelColor(Rand1, Green, 500, false)
    TurnDark
    SetPixelColor(Rand1, Blue, 500, false)
    TurnDark
  }
}
```