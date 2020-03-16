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


#custom modules
from lib import TF_IDF

app = Flask(__name__)

app.config['SECRET_KEY'] = env('APP_SECRET_KEY')
app.config['UPLOAD_PATH'] = os.getcwd() + '/data/text'
app.config['UPLOAD_ALLOWED_EXTENSIONS'] = ('.txt')

@app.route('/')
def home():
        return render_template('portal.html')

@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():

    if os.path.exists(app.config['UPLOAD_PATH']):

        shutil.rmtree(app.config['UPLOAD_PATH'])

    os.mkdir(app.config['UPLOAD_PATH'])

    if 'files[]' not in request.files:

        return redirect(request.url)

    files = request.files.getlist('files[]')

    for file in files:

        filename = secure_filename(file.filename)

        if Path(filename).suffix in app.config['UPLOAD_ALLOWED_EXTENSIONS']:

            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    return redirect('/results')

@app.route('/results')
def results():

    configs = {
        "corpus_base_file_path" : app.config['UPLOAD_PATH'],
        "corpus_file_extenions" : app.config['UPLOAD_ALLOWED_EXTENSIONS']
    }

    tf_idf = TF_IDF(**configs)

    dataframe_csv_file_path = os.path.join(tf_idf.corpus_base_file_path, 'dataframe.csv')

    if not os.path.exists(dataframe_csv_file_path):

        tf_idf.run()

        dataframe = tf_idf.dataframe

        dataframe.to_csv(dataframe_csv_file_path)

    else:

        dataframe = pd.read_csv(dataframe_csv_file_path, index_col=0)

    dataframe['sentences_in'] = dataframe.sentences_in.apply(lambda x: str(x).replace("\n","<br>"))

    dataframe['term'] = dataframe["term"].map(str) + "(" + dataframe["occurrences"].map(str) + ")"

    html = dataframe.dropna().sort_values(by='occurrences', ascending=False).head(500).drop(['weight','occurrences'], axis=1).to_html(escape=False, index=False)

    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
