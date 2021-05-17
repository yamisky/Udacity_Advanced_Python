import subprocess
import random
from typing import List

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface


class PDFIngestor(IngestorInterface):
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        temp = 'tmp/' + str(random.randint(1000, 2000)) + '.txt'
        try:
            p = subprocess.run(["pdftotext", "-layout", path, temp], timeout=2)
            with open(temp, 'r') as f:
                content = f.readlines()
        except FileNotFoundError:
            print('pdftotext tool is not availble via command line')
            return quotes

        subprocess.run(["rm", temp])

        for line in content:
            split_content = line.strip().split(' - ')
            if len(split_content) == 2:
                new_quote = QuoteModel(split_content[0], split_content[1])
                quotes.append(new_quote)

        return quotes
