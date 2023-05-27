from flask import Flask

app = Flask(__name__, template_folder="template", static_folder='static')


@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)