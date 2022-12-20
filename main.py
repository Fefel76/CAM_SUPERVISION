from flask import Flask, render_template, request, jsonify
import os
import time
import logging
import pickle
import socket

logging.basicConfig(filename='./log/supervision.log',level=logging.DEBUG,format='%(asctime)s -- %(funcName)s -- %(process)d -- %(levelname)s -- %(message)s')
app = Flask(__name__)

#TODO réseaux IP DOCKER
def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#TODO gestion mémoire via générateur yield
def get_all_images():
    image_folder = 'static'
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    images.sort()

    return images

#TODO multiple param pour gérer chaque camera
def read_param(parametres={"decoupe":10,"seuil":10,"winStride":4,"padding":4,"scale":1.1}):

    try:
        with open('./conf/param.txt', 'rb') as f:
            parametres = pickle.load(f)
    except:
        pickle.dump(parametres, open("./conf/param.txt", "wb"))
        logging.warning("pas de fichier param.txt , création par défaut")

    return parametres


#TODO tests des résultats faux-positifs
@app.route('/param', methods=["GET","POST"])
def param():
    parametres={}
    if request.method == 'POST':

        try:
            parametres['decoupe'] = request.form['decoupe']
            parametres['seuil'] = request.form['seuil']
            parametres['winStride'] = request.form['winStride']
            parametres['padding'] = request.form['padding']
            parametres['scale'] = request.form['scale']
            logging.debug(parametres)
            pickle.dump(parametres, open("./conf/param.txt", "wb"))
        except:
            logging.warning("pas de données dans le POST param")
    return render_template('param.html',parametres=read_param(),ip=get_IP())

#TODO gestion des pages
@app.route('/')
def photo():
    photos = get_all_images()
    return render_template('photo.html',photos=photos,ip=get_IP())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,  debug=False)