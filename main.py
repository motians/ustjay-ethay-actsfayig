""" Returns quote of the day in pig latin """


import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """ Get quote of the day """

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def call_the_piggy(fact_string):
    """ Send the quote to the pig latin generator. """

    url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    host = 'hidden-journey-62459.herokuapp.com'
    length = str(len(fact_string))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': host,
        'Content-Length': length
    }
    data = {'input_text': fact_string}

    pig_response = requests.post(url, headers=headers, data=data, allow_redirects=False)

    soup = BeautifulSoup(pig_response.content, "html.parser")
    pig_url = soup.find('a')

    return 'http://' + host + pig_url.get('href')


@app.route('/')
def home():
    new_fact = get_fact()
    print('new_fact={0}'.format(new_fact))
    link_to_quote = call_the_piggy(new_fact)

    return link_to_quote


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='127.0.0.1', port=port)
