from typing import List
from .IngestorInterface import IngestorInterface
from .Ingestor import Ingestor
from .CSVIngestor import CSVIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .TXTIngestor import TXTIngestor
from .QuoteModel import QuoteModel

import os

TEMP_PATH = './tmp'
STATIC_PATH = './static'

if not os.path.exists(TEMP_PATH):
    os.mkdir(TEMP_PATH)

if not os.path.exists(STATIC_PATH):
    os.mkdir(STATIC_PATH)
