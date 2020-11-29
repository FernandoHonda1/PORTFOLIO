from flask import Flask, request
from main import funcao

app = Flask('functions')
methods = ['GET', 'POST', 'PUT', 'DELETE']

@app.route('/funcao/<url>/<url1>', methods = methods)

def catch_all(url = '', url1 = ''):
    
    request.path = '/' + url + '/' + url1
    return funcao(request)

if __name__ == '__main__':
    app.run()
