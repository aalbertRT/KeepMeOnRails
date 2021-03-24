import json
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def index():
    variables = {'sncf_token': app.config['SNCF_TOKEN']}
    return render_template('index.html', **variables)

@app.route('/ajax/', methods=['POST'])
def ajax_request():
    input_form = json.loads(request.data)
    print(input_form['cityA'])
    return "OK AJAX"
