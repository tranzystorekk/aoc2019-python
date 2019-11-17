# AOC 2019 solutions

## About

This repo contains solutions to the [advent of code](https://adventofcode.com/) 2019 edition.

## [utils.parse](utils/parse.py)

This utility module provides code with a uniform way to get input,
including argument parsing.

That is, it provides an optional `-f`/`--file` flag for specifying an input file.
If this flag is not specified, input is read from stdin.

```python
from utils.parse import Parser

parser = Parser(desc="Optional assignment description")
with parser.input() as input:
    stripped = (l.strip() for l in input)
    for line in stripped:
        print(line)
```
