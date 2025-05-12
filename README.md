# 📈 Graphing Calculator – Python Turtle Implementation

**CPSC 231 – Introduction to Computer Science I**
**Assignment 2 – Fall 2021**
Author: Ryan Loi

---

## 📝 Project Overview

This assignment involved implementing a **graphing calculator** using **Python 3** and the `turtle` graphics library. Building on concepts from Assignment 1 (https://github.com/RyanLoi98/AnalyticalGeometry), this project required enhanced skills in **coordinate transformations**, **looping**, **function completion**, and **expression evaluation**.

The core objective was to complete a set of modular drawing and utility functions to generate graphical plots of user-defined expressions in a Cartesian space - just like a graphing calculator.

---

## 📐 Features & Specifications

* Draws an **800x600 pixel** chart window using `turtle`
* Allows user to:

  * Define chart **origin** (in pixels)
  * Define **scale ratio** (pixels per step)
  * Input any mathematical expression involving `x` (e.g., `x**2`, `sin(x)`)
* Automatically draws:

  * **X and Y axes** with tick marks and labels
  * **Expression curves** with proper scaling and transformation
  * Alternating **colors (red, green, blue)** for each plotted expression
* Utilizes `eval()` via a `calc()` wrapper for parsing expressions with math functions

---

## 🧠 Functions Completed

| Function Name          | Purpose                                                                 |
| ---------------------- | ----------------------------------------------------------------------- |
| `get_color(counter)`   | Alternates color (red, green, blue) for each new expression             |
| `calc_to_screen_coord` | Converts calculator coordinates to screen (pixel) coordinates           |
| `calc_minmax_x/y`      | Determines visible x/y range based on origin and ratio                  |
| `draw_x/y_axis`        | Draws x or y axis including lines, ticks, and labels                    |
| `draw_x/y_axis_tick`   | Draws tick marks at regular intervals                                   |
| `draw_x/y_axis_label`  | Renders numeric labels beside each tick                                 |
| `draw_line`            | Draws a line between two transformed points                             |
| `draw_expression`      | Evaluates and graphs the user inputted expression across visible x-axis |

---

## 🚀 How to Run

Ensure you have **Python 3.6+** installed.

```bash
python3 Graphing.py
```

Then follow these prompts in the terminal:

1. Enter origin coordinates (e.g., `400,300`)
2. Enter ratio of pixels per step (e.g., `30`)
3. Enter a math expression using `x` (e.g., `sin(x) + x**2`)
4. Repeat for more expressions, or press **Enter** on an empty prompt to quit

---

## 📸 Demo Screenshot

Here’s a screenshot of the Program in action:

![Screenshot](https://imgur.com/7ObD9lL.png)


---

## ⭐ Bonus Feature (Implemented)

* Detects and marks **local minima (orange)** and **maxima (purple)** for each expression
* Tracks and prints the **global max/min** for:

  * Each individual expression
  * All expressions across the session
* Uses `circle()` to highlight extrema locations on the chart
* Prints results to the terminal

## 🧠 Learning Outcomes

* Strengthened understanding of **coordinate systems** and **function decomposition**
* Applied **expression parsing** using `eval()` safely within controlled scope
* Learned to handle **floating-point iteration** using `while` instead of `range()`
* Practiced **modular program design** and turtle graphics rendering
* Gained insight into plotting mathematical data and identifying critical points