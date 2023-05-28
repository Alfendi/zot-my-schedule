import db
import json
import driver

from flask import Flask, redirect, url_for, render_template, request, jsonify

app = Flask(__name__, template_folder="template", static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/submitted', methods=['GET', 'POST'])
def submitted():
    if request.method == "POST":
        data = request.form.get('courseArray')
        if data is None:
            return "Failed to read data!"
        else:
            data = json.loads(data)
            score, data_list, max_diff, low_qual = driver.run(data)
            response_data = {
                'zot_score': score,
                'dropdown_text': data_list,
                'max_diff': max_diff,
                'low_qual': low_qual
            }
            return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
