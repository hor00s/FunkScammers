import spacy
from typing import Iterable
from models import Model
from praw.reddit import Redditor  # type: ignore


class BotModel(Model):
    def __init__(self, name: str) -> None:
        self.table = {
            "author": 'TEXT',
            "replied_to": 'TEXT',
            "reply_id": 'TEXT',
            "success_rate": 'INTEGER',
            "fail_rate": 'INTEGER',
        }
        super().__init__(name, **self.table)

    def comment_failed(self) -> None:
        last_id = self.fetch_last('id')
        last_success = self.fetch_last('success_rate') - 1
        last_fail = self.fetch_last('fail_rate') + 1
        self.edit(
            set=f'fail_rate={last_fail}, success_rate={last_success}',
            where=f'id={last_id}'
        )

    def comment_succeed(self) -> None:
        last_id = self.fetch_last('id')
        last_success = self.fetch_last('success_rate') + 1
        self.edit(
            set=f'success_rate={last_success}',
            where=f'id={last_id}',
        )


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
        self._nlp = spacy.load('en_core_web_lg')

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

    def is_sus(self, text: str, samples: Iterable[str],
               top_match: float, total_matches: int) -> bool:
        """Based on `en_core_web_lg` AI language proccessing model
        (more info in `references.txt`) of `spacy` library, this function
        checks whether the `text` provided matches with (more or equal)
        ammount of samples above the match rate (`top_match`)

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
        return len(
            tuple(filter(
                lambda sentence: self._nlp(sentence)
                .similarity(self._nlp(text)) > top_match, samples
            ))
        ) >= total_matches

    def delete_bad_replies(self, redditor: Redditor,
                           max_downvotes: int) -> None:
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
                self.comment_failed()
                comment.delete()

    def reply(self) -> str:
        self.comment_succeed()
        return """
TODO: Implement a reply (Include stats etc..)
        """
