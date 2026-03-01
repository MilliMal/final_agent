from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello from Flask!"


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run()
