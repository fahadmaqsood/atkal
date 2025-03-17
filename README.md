# Atkal - a Romanized Sindhi programming language

This was a semester project for the **Compiler Construction** course. I implemented an **interpreter** for a programming language that uses **Romanized Sindhi syntax**. This project explores **language localization** by allowing Sindhi speakers to write code in their native language using the Roman script.  

## Features  
- Custom **Romanized Sindhi syntax** for intuitive programming.  
- **Lexical analysis, parsing, and execution** via an interpreter.  
- Supports basic programming constructs like **variables, loops, if-else, comments and string concatenation**.  
- Implements standard **interpreter design techniques**.

## Usage
```.\atkal code.sd```

## Language syntax
- Variables
```
x = 1
y = 2

dekhaar x, y

z = x + y

dekhaar z
dekhaar x - y
```
Output
```
(1,2)
3
-1
```

- Conditions
```
z = "Fahad" + " Qazi"

// if z is Fahad then print Sahi else Galat
jekadhen (z == "Fahad") {
    dekhaar "Sahi"
}
nata {
    dekhaar "Galat"
}
```
Output
```
Galat
```

- Loops
```
x = 1

# while x is less than 10, print x and add 1 to x.
jesitaeen (x < 10) {
    dekhaar x

    x = x + 1
}
```
