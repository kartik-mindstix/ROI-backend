# from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from data_generation import summarised_data_generation
from openai_api import generate_insights_json

app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = os.path.join('datasets')
TEST_FOLDER = os.path.join('testing')
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
 
 
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEST_FOLDER'] = TEST_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def testing():
    try:
        f = request.files.get('file')
        file_name = secure_filename(f.filename)
        f.save(os.path.join(app.config['TEST_FOLDER'],
                            file_name))
        return jsonify({'message': 'Data received successfully'}),200
    except Exception as e:
        return jsonify({'error': 'No data provided','details':e}), 400

@app.route('/generate-insights',methods=['POST'])
def generate_insights():
    data = request.json
    generate_insights_json()



@app.route('/generate-master-table',methods=['POST'])
def generate_master_table():
    data = request.json
    df = pd.read_csv(f'./test/{data['filename']}')
    summarised_data_generation(df)

    return jsonify({'message':'master table created'}),200


@app.route('/submit-csv', methods=['POST'])
def handle_csv():
    f = request.files.get('file')
 
        # Extracting uploaded file name
    data_filename = secure_filename(f.filename)

    f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))
    
    return jsonify({'message':'data received succesfully'}),200



if __name__ == '__main__':
    app.run(debug=True)
