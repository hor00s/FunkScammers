import os
import praw
from praw.models.comment_forest import MoreComments
from bot import Bot
from generals import (
    Settings,
    actions,
    SCAM_SAMPLES,
    SETTINGS,
    DEF_SETTINGS,
    ascii_filter as af,
)
from dotenv import (
    find_dotenv,
    load_dotenv,
)

load_dotenv(find_dotenv())


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
            if bot.is_sus(af(post.selftext), samples, sta, tm):
                if post.author != bot.name and\
                        not bot.already_replied(post.id):
                    bot.reply('post', post.author,
                              post.id, sub_name, post)
                    print("We've a sus post in", sub_name)

            for comment in post.comments:
                if isinstance(comment, MoreComments):
                    continue
                if bot.is_sus(af(comment.body), samples, sta, tm):
                    if comment.author != bot.name and\
                            not bot.already_replied(comment.id):
                        print("We've a sus top in , sub_namelevel comment")
                        bot.reply('comment', comment.author,
                                  comment.id, sub_name, comment)

                for reply in comment.replies:
                    if isinstance(reply, MoreComments):
                        continue
                    if bot.is_sus(af(reply.body), samples, sta, tm):
                        if reply.author != bot.name and\
                                not bot.already_replied(comment.id):
                            print("We've a sus reply in", sub_name)
                            bot.reply('comment', reply.author, comment.id,
                                      sub_name, reply)
