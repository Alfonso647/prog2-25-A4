from flask import Flask, requests, jsonify
#from flask_jwt_extendend import JWTManager, create_acess_token, jwt_required, get_jwt_identity
#import hashlib

users = {}
data = {}
app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'A4'

@app.route("/")
def root():
    return 'hello world!'


if __name__ == '__main__':
    app.run(debug=True)
