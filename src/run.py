from flask import Flask
from os import getenv

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


def main():
    host = getenv('FLASK_HOST', '0.0.0.0')
    port = getenv('FLASK_PORT', 5000)
    debug = getenv('FLASK_DEBUG', 0)

    app.run(host=host, port=port, debug=debug)

if '__main__' == __name__:
    main()

