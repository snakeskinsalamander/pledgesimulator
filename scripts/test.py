from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('index')
def hello_world():
    base_element = {'title': 'Welcome to my site!', 'author': 'digitalsin'}
    return '''
    <html>
    <head>
        <title> {{ base_element.title }} </title>
    </head>
    
    <body>
        Welcome {{ baes_element.user }}
    </body>
    
    </html>
    '''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)