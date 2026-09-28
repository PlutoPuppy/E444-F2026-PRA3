import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development-only-lab-secret')
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your email address?')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        email = (form.email.data or '').strip()
        if '@' not in email:
            flash('Missing @ in email address')
        elif 'utoronto' not in email.lower():
            flash('Need to enter UofT email')
        else:
            old_name = session.get('name')
            if old_name is not None and old_name != form.name.data:
                flash('Looks like you have changed your name!')
            session['name'] = form.name.data
            session['email'] = email
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           email=session.get('email'), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
