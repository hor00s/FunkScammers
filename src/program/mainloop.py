import os
import praw
import logger
from bot import Bot
from praw.models.comment_forest import MoreComments
from praw.reddit import Submission
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
from dotenv import (
    find_dotenv,
    load_dotenv,
)


load_dotenv(find_dotenv())
log = logger.Logger(1, WORTH_LOG)


def bot_reply(post: Submission, bot: Bot, sub_name: str, type_: str) -> None:
    bot_has_replied = bot.already_replied(post.id)

    if post.author != bot.name and not bot_has_replied:
        bot.reply(type_, post.author, post.id, sub_name, post)
        print("We've a sus post in", sub_name)


@error_logger(ERROR_LOGGER)
def check_reply(text, samples, sta, tm, wl, post, bot,
                sub_name, abort_chars, submission_type):
    if bot.is_sus(af(text), samples, sta, tm, abort_chars) and text:
        bot_reply(post, bot, sub_name, submission_type)
    if bot.is_sus(af(text), samples, wl, tm, abort_chars):
        log.info(f"Saving: `{text}`")


def mainloop():
    """Mainloop of the program. This is where the actual
    bot operates.
    """
    settings = Settings(
        SETTINGS,
        **DEF_SETTINGS
    )
    settings.init()
    increment_config(settings, 'total_runs')
    reset_logs(WORTH_LOG, settings)

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
        print('iterating sub:', sub_name)
        new = reddit.subreddit(sub_name).new(limit=search_limit)
        hot = reddit.subreddit(sub_name).hot(limit=search_limit)

        for post in list(new) + list(hot):
            text = post.selftext
            check_reply(text, samples, sta, tm, wl, post,
                        bot, sub_name, abort_chars, 'post')

            for comment in post.comments:
                if isinstance(comment, MoreComments):
                    continue
                text = comment.body
                check_reply(text, samples, sta, tm, wl, post, bot,
                            sub_name, abort_chars, 'comment')

                for reply in comment.replies:
                    if isinstance(reply, MoreComments):
                        continue
                    text = reply.body
                    check_reply(text, samples, sta, tm, wl, post, bot,
                                sub_name, abort_chars, 'comment')
