import os
import praw
from praw.models.comment_forest import MoreComments
from bot import Bot
from generals import (
    Settings,
    actions,
    SCAM_SAMPLES,
    SETTINGS,
)
from dotenv import (
    find_dotenv,
    load_dotenv,
)

load_dotenv(find_dotenv())


def delete_bad_replies(redditor: praw.reddit.Redditor, max_downvotes: int):
    """Check if a reply that the bot made has less that
    `max_downvotes` and delete it

    :param redditor: An instance of the account
    :type redditor: praw.reddit.Redditor
    :param max_downvotes: The ammount of downvotes enough\
        to trigger a deletion
    :type max_downvotes: int
    """
    comments = redditor.comments.new(limit=None)

    for comment in comments:
        if comment.score < max_downvotes:
            comment.delete()


# TODO: Put an @error_log function
def mainloop():
    """Mainloop of the program. This is where the actual
    bot operates.
    """
    settings = Settings(SETTINGS)
    sus_text_above = float(settings.get('sus_text_above'))

    bot = Bot(
        username=os.environ['username'],
        password=os.environ['password']
    )

    reddit = praw.Reddit(
        client_id=os.environ['client_id'],
        client_secret=os.environ['secret'],
        password=bot.password,
        user_agent=os.environ['user_agent'],
        username=bot.name,
    )

    redditor = reddit.redditor(bot.name)

    running = True
    while running:
        delete_bad_replies(redditor, int(settings.get('max_downvotes')))
        samples = tuple(actions.load_samples(SCAM_SAMPLES))
        followed_subs = reddit.user.subreddits(limit=None)
        for sub in followed_subs:
            sub_name = str(sub)
            for post in reddit.subreddit(sub_name).new(limit=None):
                if bot.is_sus(post.selftext, samples, sus_text_above):
                    print("We've a sus post")

                for comment in post.comments:
                    if isinstance(comment, MoreComments):
                        continue
                    if bot.is_sus(comment.body, samples, sus_text_above):
                        print("We've a sus top level comment")

                        for reply in comment.replies:
                            if isinstance(reply, MoreComments):
                                continue
                            if bot.is_sus(reply.body, samples, sus_text_above):
                                print("We've a sus reply")