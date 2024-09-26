# from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from data_generation import summarised_data_generation

app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = os.path.join('datasets')
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
 
 
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-data', methods=['POST'])
def handle_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    print(f"Received data: {data}")
    return jsonify({'message': 'Data received successfully', 'received_data': data})

@app.route('/submit-csv', methods=['POST'])
def handle_csv():
    f = request.files.get('file')
 
        # Extracting uploaded file name
    data_filename = secure_filename(f.filename)

    f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))
    

    df = pd.read_csv(f'./datasets/{data_filename}')


    summarised_data_generation(df,data_filename)


    print(f)

 
    print(data_filename)
    
    return jsonify({'message':'data received succesfully'}),200



if __name__ == '__main__':
    app.run(debug=True)
