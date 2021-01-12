from flask import Flask
from bs4 import BeautifulSoup
import requests
import vobject

app = Flask(__name__)

content_lst = []


@app.route('/')
def home():
    return "Hello World"


@app.route('/find_company/<key_word>')
def find(key_word):
    html = requests.get("https://panoramafirm.pl/szukaj?k={keyword}&l=".format(keyword=key_word)).text
    soup = BeautifulSoup(html, features="html.parser")
    lst = soup.find('ul', {"id": "company-list"})
    global content_lst
    content_lst = []
    for item in lst.find_all('li', {"class": "company-item"}, recursive=False):
        name = item.find('a', {"class": "company-name"}).get_text().strip()
        address = item.find('div', {"class": "address"}).get_text().strip()
        number = item.find('a', {"class": "icon-telephone"})["title"].strip()
        email = item.find('a', {"class": "icon-envelope"})["data-company-email"].strip()
        card = vcard(name, address, number, email)
    return key_word


def vcard(name, address, number, email):
    card = vobject.vCard()
    card.add('fn')
    card.fn.value = name
    card.add('address')
    card.address.value = address
    card.add('tel')
    card.tel.value = number
    card.add('email')
    card.email.value = email
    card.email.type_param = 'INTERNET'
    return card


if __name__ == '__main__':
    app.run(debug=True)
