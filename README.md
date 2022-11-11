
![Logo](TODO...)


# ~ FunkScammers ~

A Reddit bot that works with the Reddit API through [PRAW](https://praw.readthedocs.io/en/stable/) and tries to prevent scammers in certain (and how I think, most vulnerable subreddits).



## Documentation

Version: 0.0.1 (Beta)

The application is still under construction.
More documentation will be added later!


## FAQ

#### ~ Where this bot operates?

The bot operates on the subs it folllows

#### ~ What the bot tries to detect?

The bot, with the help of [en_core_web_lg model](https://www.datasciencelearner.com/how-to-install-en_core_web_lg-spacy-model/) tries to detect posts/comments/replies (based on their [Semantic similarity](https://en.wikipedia.org/wiki/Semantic_similarity) between a bunch of samples) that seem sus and replies to them

#### ~ Why these subreddits?

The bot mostly follows *learning related* subreddits where I, as the author, personally think that enthusiastic people that want to learn something, may fall to a trap on some *great offer* / *fast learning opportunity* that seems to good to be true 




## Features

- Reply to sus posts
- Reply to sus comments 
- Reply to sus reply recursively on comments
- Delete it's own comments that have *x* number of downvotes
- And hopefully, more soon...


## Installation

Yes, this project is fully open-source and under MIT, so anyone can install it and make changes/try to tweak the settings and make it better (or worst).

Linux installation:

```bash
pip install -U pip setuptools wheel
pip install -U spacy
pip install -r requirements.txt
Spacy model: python -m spacy download en_core_web_lg
# If you see this message at the end, you're good to go
✔ Download and installation successful (If you get this msg)
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`client_id`

`Account's username`

`Account's password`

`App's name`


## Contributing

Contributions are always welcome!

Anyone may Contribute to this app by the standard *fork -> clone -> edit -> Pull request*.
See Github's very cool project: [good-first-contribution](https://github.com/firstcontributions/first-contributions) if you need any help!
You may name the branch with the following format: `<your_name>_<commit_type>`

Also make sure to run all the tests (See next section) before and after your contribution and update documentation if necessary

## Running Tests

This project is currently tested with `unittests` and it follows `mypy`'s `--strict` rules. You can take the following shortcut for type and unittesting:

```bash
  ./funkscammers unit # Run all the unittests for every module
  ./funkscammers type # To run all type cheking
  ./funkscammers allchecks # To run both unittests and typechecks
```