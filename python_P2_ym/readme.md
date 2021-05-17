# Meme Generator

## Overview of the project

The project contains code to generate a meme. It has two modes of operation.

*The command line* based version uses locally stored images to generate a meme using user supplied body text and author name. The meme is stored locally as a file and path to the file is displayed to the user.

*The web based* version can create a new meme based on user supplied image url, quote and author via a web form.
Alternatively it can generate a random meme from local images, collection of quotes and authors.
The meme is displayed in the web browser.

## Instructions for setting up 

1. Clone repository or download as a zip file.
2. From the terminal, navigate to the projects working directory `path to project\meme_generator`
3. Create a virtual environment for the project using Python 3.6+ 
4. Activate the created virtual environment
4. Use `requirements.txt` to install the dependencies for the project.
5. Create two directories inside project directory: `tmp` and `static` for storing image files. This is handled by the code.
6. You need to have `pdftotext` avaialble via commandline to us Pdf file as input for Quotes.

## Running Command line version

Use `python meme.py -h` to find the usage documentation.

The `python meme.py` the app will randomly select image or quote or the author or all the not supplied arguemnts to generate the meme. The meme image path will be displayed on the command line.

## Running web based version

### Method-1

Set the environment variable `FLASK_APP=app.py`. Then run command `flask run` to start the app server. Use the information displayed in the terminal to open the app in the web browser. Typically it will be pointing at `http://127.0.0.1:5000/`.

### Method-2
Run `python app.py`

## Sub-modules Documentation

### Module `QuoteEngine`

`QuoteEngine` defines a class `QuoteModel` for a quote format containing quote `body` text and quote `author`.

`QuoteEngine` consists of data ingestor sub-modules to extract data from `pdf`, `docx`, `txt` or `csv` format files. All supported file formats follow the common interface `IngestorInterface`. The interface provides two methods `can_ingest` and `parse`.

`can_ingest`, *classmethod*, needs path to the file including filename and it returns if the file is supported.

`parse` *classmethod*, needs path to the file and it returns collection of `QuoteModel` using extracted text from the file.

`Ingestor` provides a way to automatically select and use relevant ingestor based on the file format. 

The module is responsbile for extracting quotes from given file and provide them as a collection of `QuoteModel` objects

* To use the module, import it in your code as 
```python
from QuoteEngine import Ingestor, QuoteModel
```
Then use `Ingestor` object to extract the data from the file as a collection of `QuoteModel`. For example,

```python
if (Ingestor.can_ingest(path_to_file)):
    quotes = Ingestor.parse(path_to_file)
```

Note: PdfIngestor depends on the `pdftotext` command line utility.

### Module `MemeEngine`

`MemeEngine` module is reposnsible for:

* Opening the image file, resizing it to specified width.
* Drawing the quote at a random position on the image.
* Save the file to the disk

It implements `make_meme` method.

To use the module, import it using 
```python
from MemeEngine import MemeEngine
```

Create an instance of the `MemeEngine` and use the methd `make_meme`. For example,
```python
meme = MemeEngine(path_to_output)
meme.make_meme(path_to_image, body_text, author)
```

This module depends on `Pillow` package for image I/O and processing, in addition to the standard library.
