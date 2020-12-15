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
        name = item.find('a', {"class": "company-name"}).get_text()
        address = item.find('div', {"class": "address"}).get_text()
        number = item.find('a', {"class": "icon-telephone"})["title"]
        email = item.find('a', {"class": "icon-envelope"})["data-company-email"]
        print(name + "\n" + address + "\n" + number + "\n" + email)
    return key_word


if __name__ == '__main__':
    app.run(debug=True)
