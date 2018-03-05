from flask import Flask

from display_hello_world.config import host, port

app = Flask(__name__)


@app.route('/')
def display_hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run(host=host,
            port=port)
