# AOC 2019 solutions

## About

This repo contains solutions to the [advent of code](https://adventofcode.com/) 2019 edition.

## How to use

The files under the [days](days) directory are most conveniently run as python modules:

```shell
python3 -m days.d01p1 <input file>
```

## [utils.parse](utils/parse.py)

This utility module provides code with a uniform way to get input,
including argument parsing.

That is, it provides an optional argument for specifying an input file.
If this argument is not specified, input is read from stdin.

```python
from utils.parse import Parser

# mimics the cat utility
parser = Parser(desc="Optional assignment description")
with parser.input as input:
    stripped = (l.strip() for l in input)
    print(*stripped, sep='\n')
```
