# STACKS-IMPLEMENTATION-
ASSIGNMENT(1)_ALPHA USMAN JALLOH_905005323_BIT2101_SEM(5)
[README.md](https://github.com/user-attachments/files/33300244/README.md)

# Stack-Based Expression Evaluator

**Course:** DCOMP320 – Data Structures and Algorithms
**Assignment:** Stacks Implementation
**Student:** <ALPHA USMAN JALLOH>
**StudentID:** <905005323>

## What it does
Reads math expressions from `input.txt`, evaluates each one using a stack,
and writes the answers to `output.txt`.

## How to run
1. Install Python 3 (no extra libraries needed).
2. Put `stack_evaluator.py` and `input.txt` in the same folder.
3. Open a terminal in that folder and run:
   ```
   python stack_evaluator.py
   ```
4. Open `output.txt` to see the results.

Optional: `python stack_evaluator.py my_input.txt my_output.txt`

## Input format
- One expression per line.
- Expressions are separated by a line of dashes (`-----`).
- Supported: `+  -  *  /`, brackets `( )`, decimals, negative numbers.

```
3 + 5 * 2
(8 / 4) + 7 * 2
10 - (2 + 3) * 4
```

## Output format
Same layout as the input, with each expression replaced by its result:

```
13
16
-10
```

## How it works
Two stacks are used: one for **numbers** and one for **operators/brackets**.
Operators with higher precedence (`*`, `/`) are applied before lower ones
(`+`, `-`). Brackets are solved first.

## Assumptions and limitations
- Separator = a line containing only dashes (3 or more).
- Blank lines are ignored.
- Invalid input gives `Error: invalid expression`; dividing by zero gives
  `Error: division by zero`. The program keeps going with the next expression.
- Whole-number results print without `.0` (e.g. `13`); decimals are rounded
  to 4 places.
- Note: `(8 / 4) + 7 * 2` equals **16** (2 + 14). The assignment sheet's
  sample output shows 17, which appears to be a typo.
