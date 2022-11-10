import spacy


class Bot:
    def __init__(self, username: str, password: str) -> None:
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

    def is_sus(self, text: str, data: list[str], top_match: float) -> bool:
        return any(
            self._nlp(sentence).similarity(self._nlp(text)) > top_match
            for sentence in data
        )
