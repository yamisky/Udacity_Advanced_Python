import random
import os
import requests
from flask import Flask,render_template,abort,request
from urllib.parse import urlparse

from QuoteEngine import Ingestor
from MemeEngine import MemeEngine

app = Flask(__name__)

meme = MemeEngine('./static')



def setup():
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    imgs = None
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    static_path = './static'
    if not os.path.exists(static_path):
        os.mkdir(static_path)

    return quotes, imgs



quotes, imgs = setup()


@app.route('/', methods=[ 'GET'])
def meme_rand():
    """ Generate a random meme """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme

    Save the image from the image_url as a temp local file.
    Use MemeEngine to generate a meme using this temp file
    and the body and author form paramaters.
    Remove the temporary saved image.
    Render generated meme page.
    """
    if request.method == 'POST':
        img_url = request.form.get('image_url', default=None)
        body = request.form.get('body', default=None)
        author = request.form.get('author', default=None)

        if img_url is not None:
            response = requests.get(img_url)
            temp_file = os.path.basename(urlparse(img_url).path)
            temp_file = os.path.join('./tmp', temp_file)
            print(temp_file)
            with open(temp_file, 'wb') as fp:
                fp.write(response.content)
        path = ""
        meme = MemeEngine('./static')
        try:
            path = meme.make_meme(temp_file, body, author)
            os.remove(temp_file)
        except Exception as e:
            print(e)

    return render_template('meme.html', path=path)



if __name__ == '__main__':
    app.run()