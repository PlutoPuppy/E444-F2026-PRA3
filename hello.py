import os
import re
from datetime import datetime

from flask import Flask, flash, redirect, render_template, session, url_for, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development-only-lab-secret')
csrf = CSRFProtect(app)
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
            return redirect(url_for('chat'))
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           email=session.get('email'), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('name') or not session.get('email'):
        if request.method == 'POST':
            return {'reply': 'Please submit your name and UofT email first.'}, 401
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('chat.html')

    data = request.get_json(silent=True)
    message = data.get('message') if isinstance(data, dict) else None
    if not isinstance(message, str) or not message.strip():
        return {'reply': 'Please enter a message.'}, 400
    message = message.strip()
    if len(message) > 500:
        return {'reply': 'Please keep messages under 500 characters.'}, 400

    match = re.fullmatch(r'my name is\s+(.+)', message, re.IGNORECASE)
    if match:
        name = match.group(1).strip().rstrip('.!').strip()
        if not name or len(name) > 100:
            return {'reply': 'Please give a name between 1 and 100 characters.'}, 400
        session['chat_name'] = name
        reply = f'Nice to meet you, {name}!'
    elif message.lower().rstrip('?.!') == 'what is my name':
        name = session.get('chat_name')
        reply = f'Your name is {name}.' if name else "You haven't told me your name yet."
    elif 'hello' in message.lower():
        reply = 'Hello!'
    else:
        reply = "I don't understand. Try 'My name is Alice.' or 'What is my name?'"
    return {'reply': reply}


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))
