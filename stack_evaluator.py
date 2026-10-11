"""
DCOMP320 - Data Structures and Algorithms
Assignment: Stacks Implementation

Reads math expressions from input.txt, evaluates each one using
stacks, and writes the results to output.txt (same format as input).

Run:  python stack_evaluator.py
      python stack_evaluator.py my_input.txt my_output.txt
"""

import sys


# ---------------------------------------------------------------
# PART 1: The Stack class (push, pop, peek + helpers)
# ---------------------------------------------------------------
class Stack:
    """A simple stack: Last-In, First-Out (LIFO)."""

    def __init__(self):
        self._items = []  # a Python list stores our items

    def push(self, item):
        """Put an item on top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Look at the top item WITHOUT removing it."""
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


# ---------------------------------------------------------------
# PART 2: Parsing and evaluating an expression
# ---------------------------------------------------------------
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def tokenize(expression):
    """
    Break a string like '(8 / 4) + 7' into pieces (tokens):
    ['(', 8.0, '/', 4.0, ')', '+', 7.0]
    Also handles decimals and negative numbers like -5 or 2 * -3.
    """
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        ch = expression[i]

        if ch.isspace():  # ignore spaces
            i += 1

        elif ch.isdigit() or ch == ".":  # read a whole number
            start = i
            while i < n and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            tokens.append(float(expression[start:i]))

        elif ch in "+-*/":
            # A '-' is "unary" (a negative sign) if it comes at the start,
            # or right after another operator or an opening bracket.
            is_unary = ch == "-" and (
                    not tokens or tokens[-1] in PRECEDENCE or tokens[-1] == "("
            )
            if is_unary:
                j = i + 1
                while j < n and expression[j].isspace():
                    j += 1
                if j < n and (expression[j].isdigit() or expression[j] == "."):
                    start = j  # -5  -> the number -5
                    while j < n and (expression[j].isdigit() or expression[j] == "."):
                        j += 1
                    tokens.append(-float(expression[start:j]))
                    i = j
                else:  # -(...) -> -1 * (...)
                    tokens.append(-1.0)
                    tokens.append("*")
                    i += 1
            else:
                tokens.append(ch)
                i += 1

        elif ch in "()":
            tokens.append(ch)
            i += 1

        else:
            raise ValueError(f"invalid character '{ch}'")

    return tokens


def apply_operator(operands, operators):
    """Take one operator and two numbers off the stacks, calculate, push result."""
    op = operators.pop()
    right = operands.pop()  # the second number comes off first
    left = operands.pop()

    if op == "+":
        operands.push(left + right)
    elif op == "-":
        operands.push(left - right)
    elif op == "*":
        operands.push(left * right)
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        operands.push(left / right)


def evaluate(expression):
    """
    Evaluate an expression using TWO stacks:
      - operands  : holds the numbers
      - operators : holds + - * / and ( brackets
    This is a simplified version of Dijkstra's Shunting-Yard idea.
    """
    operands = Stack()
    operators = Stack()

    for token in tokenize(expression):

        if isinstance(token, float):  # a number
            operands.push(token)

        elif token == "(":
            operators.push(token)

        elif token == ")":
            # solve everything inside the brackets
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(operands, operators)
            if operators.is_empty():
                raise ValueError("mismatched parentheses")
            operators.pop()  # remove the '('

        else:  # + - * /
            # Before pushing, finish any earlier operator that must go first
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]):
                apply_operator(operands, operators)
            operators.push(token)

    # finish whatever is left
    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("mismatched parentheses")
        apply_operator(operands, operators)

    result = operands.pop()
    if not operands.is_empty():
        raise ValueError("invalid expression")
    return result


def format_result(value):
    """Show 13.0 as 13, and 2.5 as 2.5."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 4))


def safe_evaluate(expression):
    """Evaluate, but return a friendly message instead of crashing."""
    try:
        return format_result(evaluate(expression))
    except ZeroDivisionError:
        return "Error: division by zero"
    except (ValueError, IndexError):
        return "Error: invalid expression"


# ---------------------------------------------------------------
# PART 3: Reading input.txt and writing output.txt
# ---------------------------------------------------------------
def is_separator(line):
    """A separator is a line made only of dashes, e.g. -----"""
    return len(line) >= 3 and set(line) == {"-"}


def process_file(input_path, output_path):
    output_lines = []

    with open(input_path, "r") as infile:
        for raw_line in infile:
            line = raw_line.strip()
            if line == "":
                continue  # skip blank lines
            if is_separator(line):
                output_lines.append(line)  # keep the same separator
            else:
                output_lines.append(safe_evaluate(line))

    with open(output_path, "w") as outfile:
        outfile.write("\n".join(output_lines) + "\n")

    return output_lines


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    try:
        results = process_file(input_path, output_path)
    except FileNotFoundError:
        print(f"Could not find '{input_path}'. Put it in the same folder.")
        return

    print(f"Done! {len(results)} lines written to {output_path}")


if __name__ == "__main__":
    main()


