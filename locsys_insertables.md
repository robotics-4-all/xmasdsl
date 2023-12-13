
1. Program

```
Program {
	// Insert blocks or commands
}
```

2. Serial

```
Serial {
	// Insert blocks or commands
}
```

3. Parallel

```
// Only for serial blocks
Parallel {
	Serial {
		// Insert blocks or commands
	}
	Serial {
		// Insert blocks or commands
	}

	// Insert more serial blocks
}
```

4. Group

```
// Outside of Program. Change GROUP_NAME
Group GROUP_NAME {
	// Insert blocks or commands
}
```

5. Repeat

```
Repeat NUM_OF_TIMES {
	// Insert blocks or commands
}
```

6. SetPixelColor
```
SetPixelColor(RANGE, COLOR, DURATION, MAINTAIN=true)
```

7. Dim
```
Dim(RANGE, COLOR, DURATION, FADE_IN=false)
```

8. Rainbow
```
Rainbow(RANGE, START_COLOR, END_COLOR, DURATION, MAINTAIN=false)
```

9. Linear
```
Linear(START_RANGE, END_RANGE, START_COLOR, END_COLOR, DURATION, MAINTAIN=false)
```

10. Delay
```
Delay(DURATION)
```


12. SIMPLE EXAMPLE
```

Range Part1 [1:10:1]
Range Part2 [290:300:3]

Range Part11 [1:84:1]
Range Part22 [84:178:1]
Range Part33 [178:300:1]

Color Red [255, 0, 0]
Color Green [0, 255, 0]
Color Blue [0, 0, 255]

Group Light1 {
   Parallel {
    Serial{
      SetPixelColor(Part11, Red, 200)
    }
    Serial{
      SetPixelColor(Part22, Blue, 200)
    }
    Serial{
      SetPixelColor(Part33, Green, 200)
    }
  }
}

Group Light2 {
  Parallel {
    Serial{
      SetPixelColor(Part11, Green, 200)
    }
    Serial{
      SetPixelColor(Part22, Red, 200)
    }
    Serial{
      SetPixelColor(Part33, Blue, 200)
    }
  }
}

Group Light3 {
  Parallel {
    Serial{
      SetPixelColor(Part11, Blue, 200)
    }
    Serial{
      SetPixelColor(Part22, Green, 200)
    }
    Serial{
      SetPixelColor(Part33, Red, 200)
    }
  }
}

Program {
  Parallel {
    Serial {
      Linear(Part2, Part1, Red, Red, 2000, True)
    }
    
    Serial {
      Linear(Part1, Part2, Blue, Blue, 2000, True)
    }
  }
  
  Repeat 3 {
    Light1
    Light2
    Light3
  }
}
```
