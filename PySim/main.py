from flask import Flask, request
from flask import render_template
from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from redis import Redis
from operator import itemgetter
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'why do I need this again?'

class pledges(Form):
    name = TextField("Pledger's Name", validators=[DataRequired()])
    loc = TextField("Pledger's Location", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField("Pledge!")
    r = Redis(host='flaskpine-redis', port=6379)

    def clear_form(self):
        self.name.data = ""
        self.loc.data = ""
        self.amount.data = None

    def save_to_redis(self):
        counter = self.r.incr('pledge_count')
        # change json to string
        pl_str = json.dumps({'id': str(counter),
                             'time': str(datetime.now().strftime('%Y-%b-%d %H:%M:%S')),
                             'name': self.name.data,
                             'loc': self.loc.data,
                             'loot': self.amount.data})
        self.r.sadd('pledger', pl_str )

    # Sort keys in reverse order
    def get_redis(self):
        pledgers_ledger = []
        for item in self.r.smembers('pledger'):
            pledgers_ledger.append(json.loads(item))

        # Sort the list in reverse
        return sorted(pledgers_ledger, key=itemgetter('id'), reverse=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def pledger_world():
    form = pledges()
    base_element = {'title': 'Pledge Simulator', 'author': 'digitalsin', 'compliment': ''}
    if form.validate_on_submit():
        form.save_to_redis()
        base_element['compliment'] = 'Pledge recorded. Thanks!'

    # Read redis and dump list
    pledger_journal = form.get_redis()
    print(datetime.now())
    print(pledger_journal)

    form.clear_form()
    return render_template('index.html', base = base_element, form=form, pledger_list=pledger_journal)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)