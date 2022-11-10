import spacy
from typing import Iterable


class Bot:
    def __init__(self, username: str, password: str) -> None:
        """A bot `instance` should always work alongside with
        a `Reddit` instance

        :param username: The username (account name) of the bot
        :type username: str
        :param password: The account's password
        :type password: str
        """
        self._name = username
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

    def is_sus(self, text: str, data: Iterable[str], top_match: float) -> bool:
        """Based on `en_core_web_lg` AI language proccessing model
        (more info in `references.txt`) of `spacy` library, this function
        checks whether the `text` provided matches **at least one**
        of the samples (in range of 0.0 - 1.0) above the limit (`top_match`)

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
        :return: Wheather the sentence matched above\
            *x* with any of the samples
        :rtype: bool
        """
        return any(
            self._nlp(sentence).similarity(self._nlp(text)) > top_match
            for sentence in data
        )
