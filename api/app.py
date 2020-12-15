from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"


@app.route('/find_company/<key_word>')
def find(key_word):
    return key_word


if __name__ == '__main__':
    app.run(debug=True)
