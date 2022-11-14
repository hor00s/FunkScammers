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
        bot.check_comments(redditor, int(settings.get('max_downvotes')),
                           int(settings.get('top_upvotes')))

        samples = tuple(actions.load_samples(SCAM_SAMPLES))
        followed_subs = reddit.user.subreddits(limit=None)

        for sub in followed_subs:
            sub_name = str(sub)

            for post in reddit.subreddit(sub_name).new(limit=None):
                if bot.is_sus(af(post.selftext), samples, sta, tm):
                    if post.author != bot.name and\
                            not bot.already_replied(post.id):
                        post.reply(bot.reply('post', post.author, post.id))
                        print("We've a sus post")
                        exit()  # TODO: Remove

                for comment in post.comments:
                    if isinstance(comment, MoreComments):
                        continue
                    if bot.is_sus(af(comment.body), samples, sta, tm):
                        if comment.author != bot.name and\
                                not bot.already_replied(comment.id):
                            print("We've a sus top level comment")
                            comment.reply(bot.reply('comment', comment.author,
                                                    comment.id))
                            exit()  # TODO: Remove

                    for reply in comment.replies:
                        if isinstance(reply, MoreComments):
                            continue
                        if bot.is_sus(af(reply.body), samples, sta, tm):
                            if reply.author != bot.name and\
                                    not bot.already_replied(comment.id):
                                print("We've a sus reply")
                                reply.reply(bot.reply('comment', reply.author,
                                                      comment.id))
                                exit()  # TODO: Remove
