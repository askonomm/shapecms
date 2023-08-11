from flask import Flask

app = Flask(__name__)


@app.route("/admin")
def home():
    return "<p>Hello, World!</p>"
