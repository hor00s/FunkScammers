#!/bin/env python3
import sys
from program.program import main


"""
This program is made purely for fun in an attempt
to prevent fucking scammers from some certain
sub-reddits (The ones that are followed by the account
this bot operates on). Also this is by no means
profitable in any way and is completly open-source (as you see)!
"""


if __name__ == '__main__':
    sys.exit(
        main(*sys.argv)
    )
