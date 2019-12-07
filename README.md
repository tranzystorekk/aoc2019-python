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

## [misc.disic](misc/disic.py)

### Intcode

In this edition some tasks operate on a special Intcode language.

This module prettifies an Intcode program
by adding named operations, visual address modes and opcode positions.

### Example

For a comma-separated Intcode (wrapping added for readability):

```txt
3,52,
1001,52,-5,52,
3,53,
1,52,56,54,
1007,54,5,55,
1005,55,26,
1001,54,-5,54,
1105,1,12,
1,53,54,53,
1008,54,0,55,
1001,55,1,55,
2,53,55,53,
4,53,
1001,56,-1,56,
1005,56,6,
99,
0,
0,
0,
0,
10
```

`python3 -m misc.disic <input file>` outputs:

```txt
00000000: INP 52
00000002: ADD 52 #-5 52
00000006: INP 53
00000008: ADD 52 56 54
00000012: TLT 54 #5 55
00000016: JNZ 55 #26
00000019: ADD 54 #-5 54
00000023: JNZ #1 #12
00000026: ADD 53 54 53
00000030: TEQ 54 #0 55
00000034: ADD 55 #1 55
00000038: MUL 53 55 53
00000042: OUT 53
00000044: ADD 56 #-1 56
00000048: JNZ 56 #6
00000051: HLT
00000052: ??? (0)
00000053: ??? (0)
00000054: ??? (0)
00000055: ??? (0)
00000056: ??? (10)
```
