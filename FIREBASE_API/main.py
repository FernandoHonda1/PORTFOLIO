from flask import jsonify
import pyrebase

config = {"apiKey": "AIzaSyDeH2UTDX_fgQcaw0C1aexrndZuepzRwcM",
    "authDomain": "wine120220.firebaseapp.com",
    "databaseURL": "https://wine120220.firebaseio.com",
    "projectId": "wine120220",
    "storageBucket": "wine120220.appspot.com",
    "messagingSenderId": "152248366602",
    "appId": "1:152248366602:web:552ac9d7ac3defa1a611f3",
    "measurementId": "G-XYYCRYNPCF"}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def points_top15(url):
    
    itens_by_name = db.child("no_1").order_by_child("points").limit_to_last(int(url)).get()
    return jsonify(itens_by_name.val()), 200

def data_by_province(url):
    
    documents = db.child('no_1').order_by_child('province').equal_to(url).get()
    return jsonify(documents.val()), 200

def remove_by_timestamp(url):
    
    db.child('no_1').child(url).remove()
    return 'child {} removed'.format(url), 200 

def update_by_timestamp(url, json):
    
    db.child("no_1").child(url).update(json)
    return 'child {0} updated({1})'.format(url, json.keys()), 200

def funcao(request):
    
    if request.path.startswith('/'):
        full_url = request.path.split('/')
    
        if request.method == 'GET':

            if full_url[1] == 'top' and full_url[2] is not None:
                return points_top15(full_url[2])

            elif full_url[1] == 'province' and full_url[2] is not None:
                return data_by_province(full_url[2])
   

        elif request.method == 'DELETE' and full_url[1] == 'delete' and full_url[2] is not None:
            return remove_by_timestamp(full_url[2])
        
        elif request.method == 'PUT' and full_url[1] == 'update' and full_url[2] is not None:
            json = request.json
            return update_by_timestamp(full_url[2], json)
    
        else:
            return 'Método não suportado.', 400    
        return 'URL não encontrada.', 400
    
