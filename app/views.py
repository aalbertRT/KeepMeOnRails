from flask import Flask, render_template, url_for

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def index():
    variables = {'sncf_token': app.config['SNCF_TOKEN']}
    return render_template('index.html', **variables)

