# Spelling with Chemistry
Daily Programmer challenge #302: [link](https://www.reddit.com/r/dailyprogrammer/comments/5seexn/20170206_challenge_302_easy_spelling_with/)

Implemented bonus challenge of sorting multiple solutions by atomic weight, and also implemented "fuzzy matching".

## Setup

Requires Python3 and the following modules:

* logging
* argparse
* pandas

## Usage

    ➤ python3 chemistry.py --help
     usage: chemistry.py [-h] [-d] [-v] [-f]
    
    optional arguments:
      -h, --help     show this help message and exit
      -d, --debug    Print all debug output (for devs)
      -v, --verbose  Print info messages (for users)
      -f, --fuzzy    Allow fuzzy matching for flexible spelling

A copy of the periodic table, including Element, Symbol, Atomic Number, Atomic Weight, and Electronegativity is provided in the `data/` folder. It is consumed by default by the `PeriodicTable` class.

While running, the program will continuously prompt for a new string input and attempt to translate the text into chemical symbols. There is no "STOP" command, so exit the program by sending a KeyboardInterrupt such as Ctrl-C.

## Fuzzy Matching

When `--fuzzy` is enabled, the program will skip unmatchable characters and continue recursing. This has the downside of double-counting results, but can be used to extend chemical chains and spell complete sentences (with punctuation and spaces) into chemical characters.

    ➤ python3 chemistry.py
    word: breaking bad
    CRITICAL:root:Cannot match next symbols 'a' 'k'
    CRITICAL:root:Cannot match next symbols 'e' 'a'
    The input cannot be spelled with chemistry.
    
    ➤ python3 chemistry.py --fuzzy
    word: breaking bad
    BReKINBa (Boron, Rhenium, Potassium, Iodine, Nitrogen, Barium)

## Debugging

There is a `--verbose` mode which sets log level to "INFO" and prints one line for every finished continuation chain, then once again with the line's atomic weight.

There is a `--debug` mode which sets log level to "DEBUG" and prints very fine-grained log messages including branching factors, accumulator results, configuration settings, and sorting logic.

