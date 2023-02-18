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
    SETTINGS,
    BASE_DIR,
    ascii_filter as af,
)
from dotenv import (
    find_dotenv,
    load_dotenv,
)


load_dotenv(find_dotenv())
log = logger.Logger(1, f"{BASE_DIR}/.logs.txt")


def bot_reply(post: Submission, bot: Bot, sub_name: str, type_: str) -> None:
    if post.author != bot.name and not bot.already_replied(post.id):
        bot.reply(type_, post.author, post.id, sub_name, post)
        print("We've a sus post in", sub_name)


def mainloop():
    """Mainloop of the program. This is where the actual
    bot operates.
    """
    settings = Settings(
        SETTINGS,
        **DEF_SETTINGS
    )
    settings.init()
    # Just 2 alliases for these long-ass variable names
    sus_text_above = sta = float(settings.get('sus_text_above'))  # noqa
    total_matches = tm = int(settings.get("total_matches"))  # noqa
    worth_logging = wl = float(settings.get('worth_logging'))  # noqa

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
            if bot.is_sus(af(text), samples, sta, tm) and text:
                bot_reply(post, bot, sub_name, 'post')
            if bot.is_sus(text, samples, wl, tm):
                log.info(f"Saving: `{text}`")

            for comment in post.comments:
                if isinstance(comment, MoreComments):
                    continue
                text = comment.body
                if bot.is_sus(af(text), samples, sta, tm) and text:
                    bot_reply(comment, bot, sub_name, 'comment')
                if bot.is_sus(text, samples, wl, tm):
                    log.info(f"Saving: `{text}`")

                for reply in comment.replies:
                    if isinstance(reply, MoreComments):
                        continue
                    text = reply.body
                    if bot.is_sus(af(text), samples, sta, tm) and text:
                        bot_reply(comment, bot, sub_name, 'comment')
                    if bot.is_sus(text, samples, wl, tm):
                        log.info(f"Saving: `{text}`")
