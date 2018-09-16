""" Hack MIT project 9/15/18
    Andrea Zavala, Trevor Nogués, and John Lentfer
    Harvey Mudd College """

""" Our project creates a webpage that takes in a word input
    and outputs a series of gifs that explore relates topics """

import os
from flask import render_template, Flask, request
import giphy_client
import urllib,json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def substring_after(s, delim):
        return s.partition(delim)[2]

    def substring_before(s, delim):
        return s.partition(delim)[0]

    def getLinks(depth, wikiLinks):
        if depth < 6:
            pageUrl = wikiLinks[-1]
            html = urlopen("https://en.wikipedia.org"+pageUrl)
            bsObj = BeautifulSoup(html, "html.parser")
                    #for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")): counter +=1
            link = random.choice(bsObj.findAll("a", href=re.compile("^(/wiki/)")))
            print (type(link))
            wikiLinks.append(str(link['href']))
            return getLinks(depth + 1, wikiLinks)
        else:
            return wikiLinks

    @app.route('/start')
    def start():
        return render_template('gif.html', name = '')

    @app.route('/')
    def index():
        return render_template('gif.html')

    @app.route('/hello', methods=['POST'])
    def hello():
        first_name = request.form['first_name']
        line = first_name.replace(' ', '_')
        wikiLinks = getLinks(0, ['/wiki/'+line])
        a = []
        b = []
        for i in range(len(wikiLinks)):
            line2 = wikiLinks[i]
            temp = (wikiLinks[i][6:])
            line3 = temp.replace('_', ' ')
            b.append(line3)
            print(wikiLinks)
            data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q=" + line2 + "&api_key=Hve1mDgMnLGS50ZCOIwzV415RZwm3NI7&limit=1").read())
            x = json.dumps(data, sort_keys=True, indent=4)
            y = substring_after(x, '"embed_url": "')
            z = substring_before(y, '",')
            if line2 == 'skrazapod':
                z = 'https://items.jellyneo.net/assets/imgs/items/32864.gif?706'
            a.append(z)

        print(a)

        return (render_template('gif2.html', name = a, wikiLinks = b))

    return app
