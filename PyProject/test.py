from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def hello_world():
    base_element = {'title': 'Pledge Simulator', 'author': 'digitalsin'}
    return render_template('index.html', base = base_element)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)