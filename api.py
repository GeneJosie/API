from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Route GET simple
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Salut depuis l'API Flask !"})

if __name__ == '__main__' : 
    app.run(debug=True)