import os
import praw  # type: ignore
import logger
from bot import Bot
from praw.models.comment_forest import MoreComments  # type: ignore
from praw.reddit import Submission  # type: ignore
from generals import (
    Settings,
    actions,
    SCAM_SAMPLES,
    DEF_SETTINGS,
    ERROR_LOGGER,
    SETTINGS,
    WORTH_LOG,
    ascii_filter as af,
    error_logger,
    increment_config,
    reset_logs,
)
from dotenv import (  # type: ignore
    find_dotenv,
    load_dotenv,
)
from typing import (
    List,
    Literal,
    Generator,
)


load_dotenv(find_dotenv())
log = logger.Logger(1)
logs: List[str] = []


def bot_reply(post: Submission, bot: Bot, sub_name: str, type_: str) -> None:
    bot_has_replied = bot.already_replied(post.id)
    is_stickied = post.is_stickied
    print(is_stickied)
    if post.author != bot.name and not bot_has_replied:
        bot.reply(type_, post.author, post.id, sub_name, post)
        log.info("We've a sus post in", sub_name)


@error_logger(ERROR_LOGGER)
def check_reply(text: str, samples: Generator[str, None, None], sta: float,
                tm: int, wl: float, post: Submission, bot: Bot, sub_name: str, logs: List[str],
                abort_chars: List[str], submission_type: Literal["post", "comment"]) -> None:

    if bot.is_sus(af(text), samples, sta, tm, abort_chars) and text:
        bot_reply(post, bot, sub_name, submission_type)
    if bot.is_sus(af(text), samples, wl, tm, abort_chars):
        logs.append(text)


def mainloop() -> None:
    """Mainloop of the program. This is where the actual
    bot operates.
    """
    settings = Settings(
        SETTINGS,
        **DEF_SETTINGS
    )
    settings.init()
    increment_config(settings, 'total_runs')
    reset_logs(str(WORTH_LOG), settings)

    # Just 2 alliases for these long-ass variable names
    sus_text_above = sta = float(settings.get('sus_text_above'))  # noqa
    total_matches = tm = int(settings.get("total_matches"))  # noqa
    worth_logging = wl = float(settings.get('worth_logging'))  # noqa
    abort_chars = settings.get('abort_chars')

    bot = Bot(
        username=os.environ['username'],
        password=os.environ['password'],
    )

    reddit = praw.Reddit(
        client_id=os.environ['client_id'],
        client_secret=os.environ['secret'],
        password=bot.password,
        user_agent=os.environ['user_agent'],
        username=bot.name,
    )

    bot.create_table()
    redditor = reddit.redditor(bot.name)

    bot.check_comments(redditor, int(settings.get('max_downvotes')),
                       int(settings.get('top_upvotes')))

    search_limit = int(settings.get('max_posts_lookup'))

    samples = tuple(actions.load_samples(SCAM_SAMPLES))
    followed_subs = reddit.user.subreddits(limit=None)

    for sub in followed_subs:
        sub_name = str(sub)
        log.info(f'Iterating sub: {sub_name}')
        new = reddit.subreddit(sub_name).new(limit=search_limit)
        hot = reddit.subreddit(sub_name).hot(limit=search_limit)

        for post in list(new) + list(hot):
            text = post.selftext
            check_reply(text, samples, sta, tm, wl, post,
                        bot, sub_name, logs, abort_chars, 'post')

            for comment in post.comments:
                if isinstance(comment, MoreComments):
                    continue
                text = comment.body
                check_reply(text, samples, sta, tm, wl, post, bot,
                            sub_name, logs, abort_chars, 'comment')

                for reply in comment.replies:
                    if isinstance(reply, MoreComments):
                        continue
                    text = reply.body
                    check_reply(text, samples, sta, tm, wl, post, bot,
                                sub_name, logs, abort_chars, 'comment')

    # At the end of the program append all logs in the file
    logs_as_text = '\n'.join(logs)
    with open(WORTH_LOG, mode='a') as f:
        f.write(logs_as_text)
        f.write('\n')
    log.info("All posts have been checked. Program is over")
