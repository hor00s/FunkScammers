#!/bin/env python3
import sys
from program.program import main  # type: ignore
from bot.bot import Bot
from generals.constants import SCAM_SAMPLES
from generals.actions import load_samples

"""
This program is made purely for fun in an attempt
to prevent fucking scammers from some certain
sub-reddits (The ones that are followed by the account
this bot operates on). Also this is by no means
profitable in any way and is completly open-source (as you see)!
"""


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        # python3 funkscammers.py test "A random sentence"
        samples = load_samples(SCAM_SAMPLES)

        bot = Bot('username', 'password')
        for sample in samples:
            sentence = sys.argv[2]
            rate = bot.get_rate(sample, sentence)
            print(f'{sentence = }\n{sample = }\n{rate = }\n')
        sys.exit(0)

    sys.exit(
        main(*sys.argv)
    )
