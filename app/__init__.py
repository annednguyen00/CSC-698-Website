from flask import Flask

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

from app import routes, errors, us, world, predictions

if __name__ == "__main__":
    app.run()