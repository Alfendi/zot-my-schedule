from flask import Flask, redirect, url_for, render_template, request, jsonify
import db

app = Flask(__name__, template_folder="template", static_folder='static')


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html', list=db.get_cached())
    # return render_template('index.html')

@app.route('/submitted', methods=['POST', 'GET'])
def submitted():
    data = request.form['data']
    new_content = "New content based on the submitted data"
    return jsonify({'content': new_content})

if __name__ == "__main__":
    app.run(debug=True)