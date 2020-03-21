import os
import shutil
from flask import Flask, redirect, render_template, request, session, url_for
from envs import env
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
import pandas as pd
from pathlib import Path



app = Flask(__name__)

app.config['SECRET_KEY'] = env('APP_SECRET_KEY')

@app.route('/')
def home():
        return render_template('portal.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
