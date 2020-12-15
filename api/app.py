from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"


@app.route('/find_company/<key_word>')
def find(key_word):
    html = requests.get("https://panoramafirm.pl/szukaj?k={keyword}&l=".format(keyword=key_word)).text
    soup = BeautifulSoup(html, features="html.parser")
    lst = soup.find('ul', {"id": "company-list"})
    for item in lst.find_all('li', {"class": "company-item"}, recursive=False):
        name = item.find('div', {"class": "company-top-content"}).find('div').find('h2').find('a').get_text()
        print(name)
    return key_word


if __name__ == '__main__':
    app.run(debug=True)
