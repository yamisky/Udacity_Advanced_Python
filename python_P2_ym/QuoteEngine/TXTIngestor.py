
from typing import List

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface

"""Reads quote from a text file
One quote per line.
body and author are separated by ' - '
"""


class TXTIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []

        with open(path, 'r') as f:
            data = f.readlines()
        for line in data:
            if line != "":
                parse = line.strip().split(' - ')
                new_quote = QuoteModel(parse[0], parse[1])
                quotes.append(new_quote)

        return quotes
