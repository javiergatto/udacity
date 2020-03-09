import os
import shutil
from flask import Flask, redirect, render_template, request, session, url_for
from envs import env
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename


#custom modules
from lib import TF_IDF

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkeygoeshere'
app.config['UPLOAD_PATH'] = os.getcwd() + '/data/text'
app.config['UPLOAD_ALLOWED_EXTENSIONS'] = ['txt']

@app.route('/')
def home():
    return render_template('portal.html')

@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    shutil.rmtree(app.config['UPLOAD_PATH'])
    os.mkdir(app.config['UPLOAD_PATH'])
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_ALLOWED_EXTENSIONS']:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return redirect('/results')

@app.route('/results')
def results():

    configs = {
        "corpus_base_file_path" : app.config['UPLOAD_PATH'],
        "corpus_file_extenions" : ('.txt')
    }
    
    tf_idf = TF_IDF(**configs)
    tf_idf.run()

    dataframe = tf_idf.term_frequency_inverse_document_frequency_df

    html = dataframe.sort_values(by='weight', ascending=False).head(30).to_html()

    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
