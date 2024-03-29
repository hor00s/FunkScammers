from logger import Logger
from models import Model
from typing import (
    Generator,
    Iterable,
    Tuple,
    List,
)
from praw.reddit import (  # type: ignore
    Redditor,
    Submission
)
from generals import (
    Settings,
    total_samples,
    is_imported,
    DEF_SETTINGS,
    SCAM_SAMPLES,
    SETTINGS,
)

settings = Settings(
    SETTINGS,
    **DEF_SETTINGS
)
settings.init()

log = Logger(1)

try:
    import spacy  # type: ignore
except ModuleNotFoundError:
    from difflib import SequenceMatcher
    log.debug("Running with `SequenceMatcher`")
else:
    log.debug("Running with `spacy`")


__all__ = [
    'Bot'
]


class BotModel(Model):
    def __init__(self, name: str) -> None:
        self.table = {
            "author": 'TEXT',
            "reply_id": 'TEXT',
            "success_rate": 'INTEGER',
            "fail_rate": 'INTEGER',
            "subs_name": "TEXT",
        }
        super().__init__(name, **self.table)

    def comment_failed(self) -> None:
        """Edit the last entry inserted by adding one (1) to
        `fail_rate` and substracting one (1) from `success_rate`
        """
        try:
            # TODO: Maybe I should also remove the 'said comment' by `reply_id`
            # but then, I might lose track of success/fail rate..
            last_id = self.fetch_last('id')
            last_success = self.fetch_last('success_rate') - 1
            last_fail = self.fetch_last('fail_rate') + 1
            self.edit(
                set=f'fail_rate={last_fail}, success_rate={last_success}',
                where=f'id={last_id}'
            )
        except IndexError:
            log.debug('No comments have been inserted yet')

    def insert_reply(self, author: str, rep_id: str, subs_name: str) -> None:
        """Insert a reply to the database

        :param auth: The name of the redditor that made the comment/post
        :type auth: str
        :param rep_id: "Scammer's" comment/post id
        :type rep_id: str
        :param subs_name: The name of the sub the comment/post was found
        :type subs_name: str
        """
        if not self.fetch_all():
            # If the database is empty, we initialize success and fail rates
            self.insert(author=author, reply_id=rep_id,
                        success_rate=1, fail_rate=0, subs_name=subs_name)
        else:
            # Otherwhise we use the proper counter
            s_rate = self.fetch_last('success_rate') + 1
            f_rate = self.fetch_last('fail_rate')
            self.insert(author=author, reply_id=rep_id,
                        success_rate=s_rate, fail_rate=f_rate,
                        subs_name=subs_name)

    def worst_sub(self, col: str = 'subs_name') -> Tuple[str, int]:
        """This function will count all the subs that the bot
        has replied and return whichever it has replied the most

        :param col: The col of the row, defaults to 'subs_name'
        :type col: str, optional
        :return: ('sub_name' total_replies) if the db is not empty
        else ('', 0) (a falsy tuple)
        :rtype: tuple[str, int]
        """
        counter = {}
        replies = self.fetch_all()
        for reply in replies:
            sub_name = self.filter_row(reply, col)
            if sub_name not in counter:
                counter[sub_name] = 0
            else:
                counter[sub_name] += 1

        try:
            k = max(counter, key=counter.get)  # type: ignore
            v = counter[k]
        except ValueError:
            log.debug('database is empty')
            # Keep the return value consistent by returning a `falsy` tuple
            return ('', 0)
        else:
            # (sub_name, ammount_of_replies)
            return (k, v)


class Bot(BotModel):
    def __init__(self, username: str, password: str) -> None:
        """A bot `instance` should always work alongside with
        a `Reddit` instance

        :param username: The username (account name) of the bot
        :type username: str
        :param password: The account's password
        :type password: str
        """
        super().__init__(username)
        self._passwd = password

    def __str__(self) -> str:
        return str(self._name)

    def __repr__(self) -> str:
        return f"<Bot({self._name})>"

    @property
    def name(self) -> str:
        return self._name

    @property
    def password(self) -> str:
        return self._passwd

    def _parse_text(self, text: str) -> Generator[str, None, None]:
        return map(  # type: ignore
            lambda i: i[:-1] if i.endswith('.') or i.endswith(',') else i,
            [word.lower() for sentence in text.split(' ')
            for word in sentence.split('\n') if word]  # noqa
        )

    def text_is_s(self, text: str, abort_chars: List[str]) -> bool:
        return any(i in abort_chars for i in self._parse_text(text))

    def already_replied(self, comment_id: str) -> bool:
        return bool(
            self.filter("reply_id", f"'{comment_id}'")
        )

    def get_rate(self, sentence, text):
        if is_imported('spacy'):
            nlp = spacy.load('en_core_web_lg')
            rate = nlp(sentence).similarity(nlp(text))
        else:
            rate = SequenceMatcher(None, sentence, text).ratio()
        return rate

    def is_sus(self, text: str, samples: Iterable[str], top_match: float,
               total_matches: int, abort_chars: List[str]) -> bool:
        """Top part: Based on `en_core_web_lg` AI language proccessing model
        (more info in `references.txt`) of `spacy` library, this function
        checks whether the `text` provided matches with (more or equal)
        ammount of samples above the match rate (`top_match`)

        Bottom part: Works about the same way but it uses a class from
        a very lightweight built-in library (`SequenceMatcher`) to achive
        the same thing. Mostly for testing purposes (for now) and in an
        effort to free the program from the huge dependency of `spacy`
        and `en_core_web_lg`

        (This may change in the future based on the success rate of the
        bot to match **at least two** above the limit)

        :param text: The sentence which will be matched\
            agnainst the `data`
        :type text: str
        :param data: The stored samples which the bot\
            trains on
        :type data: Iterable[str]
        :param top_match: The matching rate (0.0 - 1.0)\
            that the bot detects
        :type top_match: float
        :param total_matches: The total ammount of samples the `text`\
            needs to be matched agnainst in order to be tagged as sus
        :type data: Iterable[str]
        :return: Wheather the sentence matched above\
            *x* with any of the samples
        :rtype: bool
        """
        if not self.text_is_s(text, abort_chars):
            local_matches = tuple(filter(
                lambda sentence: self.get_rate(sentence, text) > top_match, samples
            ))
            return len(local_matches) >= total_matches

    def check_comments(self, redditor: Redditor,
                       max_downvotes: int, max_upvotes: int) -> None:
        """Check if a reply that the bot made has less that
        `max_downvotes` and delete it

        :param redditor: An instance of the account
        :type redditor: praw.reddit.Redditor
        :param max_downvotes: The ammount of downvotes enough\
            to trigger a deletion
        :type max_downvotes: int
        """
        comments = redditor.comments.new(limit=None)
        log.info("Checking my old comments")
        for comment in comments:
            if comment.score < max_downvotes:
                log.info("Bad comment found")
                self.comment_failed()
                comment.delete()
            elif comment.score > max_upvotes:
                log.info("Saving reply")
                # TODO: Save text

    def get_success_percentage(self, failed: int, succesed: int) -> float:
        """Based on the failed and succesful replies, return the
        success percentage of the bot

        TODO: I'm not sure about the accuracy of this function

        :param failed: Total bad replies
        :type failed: int
        :param succesed: Total good replies
        :type succesed: int
        :return: The total percentage between good and bad
        :rtype: float
        """
        total_replies = failed + succesed
        rate = (1 - (failed / total_replies)) * 100
        return float(f"{rate:.2f}")

    def reply(self, type_: str, user: Redditor,
              reply_id: str, sub_name: str, comment: Submission) -> None:
        """Posts the proper reply for a sus submission

        :param type_: The type of text the bot replies to (post/comment)
        :type type_: str
        :return: The formatted reply that will be posted on Reddit
        :rtype: str
        :Raises AsserionError: As a safety mechanism in case `type_`
            argument is invalid
        """
        types = ('comment', 'post')
        assert type_.lower() in types,\
            f"Invalid argument type `{type_}`. Expected: {' or '.join(types)}"

        # Added this check because if an account gets deleted but the comment
        # stays, bot attepts to reply but `user` ends up being `None`
        # thus giving an `AttributeError`
        if user.name is not None:
            self.insert_reply(user.name, reply_id, sub_name)
            s_rate = self.fetch_last('success_rate')
            f_rate = self.fetch_last('fail_rate')

            samples = total_samples(SCAM_SAMPLES)
            sub_name, replies = self.worst_sub()
            # Remember, if the database is empty,
            # `sub_name` and `replies` will be `falsy`

            comment.reply(f"""
Based on {samples} samples I've gathered so far,
this {type_} is highly sus and probably a scam. If you think this is right,
please consider reporting u/{user.name}. If you disagree, downvote my reply
and this comment will delete it self automatically!

^(My current rating is: {self.get_success_percentage(f_rate, s_rate)}%%\
%s)

---
^(I'm a bot and this action was performed automatically. Check out \
my) [^source ^code](https://github.com/hor00s/FunkScammers) ^(and feel free \
to make any suggestions to make me better!)
        """ % (f" | worst sub so far: **{sub_name}** with **{replies}** \
total scams detected" if sub_name and replies else '',))
