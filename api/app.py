from flask import Flask, Response, render_template
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
        dct = {
            "name": name,
            "address": address,
            "number": number,
            "email": email,
            "card": card
        }
        content_lst.append(dct)
    return render_template('page.html', data=content_lst)


@app.route('/download/<id>')
def download(id):
    card = content_lst[int(id)]["card"]
    return Response(card.serialize(), mimetype="text/json+application+vcard",
                    headers={"Content-Disposition": "attachment;filename=card.vcf",
                             "Content-Transfer-Encoding": "binary"})


def vcard(name, address, number, email):
    card = vobject.vCard()
    card.add('fn')
    card.fn.value = name
    card.add('address')
    card.address.value = address
    card.address.type_param = 'WORK'
    card.add('tel')
    card.tel.value = number
    card.tel.type_param = 'WORK'
    card.add('email')
    card.email.value = email
    card.email.type_param = 'INTERNET'
    return card


if __name__ == '__main__':
    app.run(debug=True)
