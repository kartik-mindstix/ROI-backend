from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>hello</h1>'
@app.route('/submit-data', methods=['POST'])
def handle_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    print(f"Received data: {data}")
    return jsonify({'message': 'Data received successfully', 'received_data': data})

if __name__ == '__main__':
    app.run(debug=True)
