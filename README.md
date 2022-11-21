
![Logo](TODO...)


# ~ FunkScammers ~

A Reddit bot that works with the Reddit API through [PRAW](https://praw.readthedocs.io/en/stable/) and tries to prevent scammers in certain (and how I think, most vulnerable subreddits).



## Documentation

Version: 0.0.1 (Beta)

The application is still under construction.
More documentation will be added later!


## FAQ

#### ~ Where this bot operates?

The bot operates on the subs it folllows. It mainly targets *learning x* subs where I think people are more *vulnerable* because it can step upon people's frustration and willing to learn.

#### ~ What the bot tries to detect?

The bot, with the help of [en_core_web_lg model](https://www.datasciencelearner.com/how-to-install-en_core_web_lg-spacy-model/) tries to detect posts/comments/replies (based on their [Semantic similarity](https://en.wikipedia.org/wiki/Semantic_similarity) between a bunch of samples) that seem sus and replies to them

#### ~ Why these subreddits?

The bot mostly follows *learning related* subreddits where I, as the author, personally think that enthusiastic people that want to learn something, may fall to a trap on some *great offer* / *fast learning opportunity* that seems to good to be true.

## Features

- Reply to sus posts
- Reply to sus comments recursively
- Delete it's own comments that have *x* number of downvotes
- Keep track of it's score
- Keep track of the sub with the bigger ammount of sus submissions found
- And hopefully, more soon...

## Installation

Anyone may install this program and make changes/try to tweak the settings and make it better (or worst)!

Linux installation:

```bash
pip install -U pip setuptools wheel
pip install -U spacy
pip install -r requirements.txt
Spacy model: python -m spacy download en_core_web_lg
# If you see this message at the end, you're good to go
✔ Download and installation successful (If you get this msg)
```

### Minimal installation

In-case of minimal installation the bot will exclude spacy and will
automatically run with built-in `SequenceMatcher` class

```
pip install minimal-requirements.txt
# Optionally
pip install mypy
```

### Why use one installation over the other
`SequenceMatcher` pros:
- Built-in
- Way less hardware demanding
- Way smaller memory-wise

`SequenceMatcher` cons:
- Calculations are purely algorithmic and will not account for the *context* of a sentence

`Spacy` pros:
- Calculatios are done by Machine Learning model ([en_core_web_lg](https://spacy.io/models/en))
- Will attempt to understand the context of the a sentence

`Spacy` cons:
- *Heavy* memory wise
- More **hardware demading**


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Reddit's client id (`client_id`)
- Reddit's secret key  (`secret`)
- Account's username (`username`)
- Reddit's provided user agent (`user_agent`)
- Account's password (`password`)

## Contributing

Contributions are always welcome!

**Always in need of more samples (See `samples.csv`)**

- Python version used: 3.10.x
- Pip version used: 22.3.x

Anyone may Contribute to this app by the standard *fork -> clone -> edit -> Pull request*.

See Github's very cool project [good-first-contribution](https://github.com/firstcontributions/first-contributions) if you need any help for the steps you have to take!

You may name the branch with the following format: `<your_name>_<commit_type>`

Make sure to run all the tests (See next section) before and after your changes and update documentation if necessary.
It's also worth mentioning that the program follows the `sphinx` docstring format.

Finally, contributors may add their name with a hyperlink to their profile at the **Contributors** section at  the bottom of this file!

### Ideas for contribution
- Provide some scam posts/comments for the bot
- Add some more logging around the application
- Find/Make a cool logo and put it at the top of this file
- Finish the cli with whatever tool you feel comfortable with (`argaparse`, `click` etc.. you name it)
- Write better docstrings throughout the functions/classes
- Make the documentation better
- Refactor the `src/program/mainloop.py`

## Running Tests

This project is currently tested with `unittest` and it follows `mypy`'s `--strict` rules. You can take the following shortcut for type and unittesting:

```bash
  ./funkscammers unit      # Run all the unittests for every module
  ./funkscammers type      # To run all type cheking for every module
  ./funkscammers allchecks # To run both unittests and typechecks
```

## Authors
* [hor00s](https://github.com/hor00s)

## Contributors
* N/A

## Worthy mentions
* u/BicarbonateOfSofa
