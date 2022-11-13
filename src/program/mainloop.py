import os
import praw
from praw.models.comment_forest import MoreComments
from bot import Bot
from generals import (
    Settings,
    actions,
    SCAM_SAMPLES,
    SETTINGS,
    ERROR_LOGGER,
    ascii_filter as af,
)
from dotenv import (
    find_dotenv,
    load_dotenv,
)

load_dotenv(find_dotenv())


@actions.error_logger(ERROR_LOGGER)
def mainloop():
    """Mainloop of the program. This is where the actual
    bot operates.
    """
    settings = Settings(SETTINGS)
    # Just 2 alliases for these long-ass variable names
    sus_text_above = sta = float(settings.get('sus_text_above')) # noqa
    total_matches = tm = int(settings.get("total_matches")) # noqa

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

    running = True
    while running:
        print('mainloop started')
        bot.delete_bad_replies(redditor, int(settings.get('max_downvotes')))
        samples = tuple(actions.load_samples(SCAM_SAMPLES))
        followed_subs = reddit.user.subreddits(limit=None)
        for sub in followed_subs:
            sub_name = str(sub)
            for post in reddit.subreddit(sub_name).new(limit=None):
                if bot.is_sus(af(post.selftext), samples, sta, tm):
                    print("We've a sus post")
                    print(post.selftext)

                for comment in post.comments:
                    if isinstance(comment, MoreComments):
                        continue
                    if bot.is_sus(af(comment.body), samples, sta, tm):
                        print("We've a sus top level comment")
                        print(comment.body)

                        for reply in comment.replies:
                            if isinstance(reply, MoreComments):
                                continue
                            if bot.is_sus(af(reply.body), samples, sta, tm):
                                print("We've a sus reply")
                                print(reply.body)
