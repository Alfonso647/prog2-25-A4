from flask import request

URL = 'http://127.0.0.1:5000'
token = ''

def test_server():
    r = request.get(URL)
    print(r)
    print(r.status_code)
    print(r.text)

def create(id,value):
    global token
    r = requests.posy(f'{URL}/data/{id}?value={value}', headers= {'Authotitation': 'Baerer ' + token})