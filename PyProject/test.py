from flask import Flask, request
from flask import render_template
from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from redis import Redis

import random
import string


app = Flask(__name__)
app.config['SECRET_KEY'] = 'why do I need this again?'

class pledges(Form):
    name = TextField("Pledger's Name", validators=[DataRequired()])
    loc = TextField("Pledger's Location", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField("Pledge!")
    r = Redis(host='127.0.0.1', port=6379)

    def clear_form(self):
        self.name.data = ""
        self.loc.data = ""
        self.amount.data = None

    def save_to_redis(self):
        counter = self.r.incr('pledge_count')
        self.r.rpush('pledger:' + str(counter), self.name.data)
        self.r.rpush('pledger:' + str(counter), self.loc.data)
        self.r.rpush('pledger:' + str(counter), self.amount.data)

    # Change keys
    def get_redis(self):
        pledgers_ledger = {}
        for item in self.r.keys('pledger:*'):
            pledgers_ledger[item] = (self.r.lrange(str(item),0,2))
        return pledgers_ledger


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def hello_world():
    form = pledges()
    base_element = {'title': 'Pledge Simulator', 'author': 'digitalsin', 'compliment': ''}
    pledger_journal = form.get_redis()
    if form.validate_on_submit():
        form.save_to_redis()
        base_element['compliment'] = 'Pledge recorded. Thanks!'
        print(pledger_journal)
    form.clear_form()
    return render_template('index.html', base = base_element, form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)