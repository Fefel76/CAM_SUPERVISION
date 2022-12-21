from flask import Flask, render_template, request, jsonify
import os
import time
import logging
import pickle
import socket

logging.basicConfig(filename='./log/supervision.log',level=logging.DEBUG,format='%(asctime)s -- %(funcName)s -- %(process)d -- %(levelname)s -- %(message)s')
app = Flask(__name__)



#TODO réseaux IP DOCKER cf network
def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return "192.168.1.18"
    #return s.getsockname()[0]


def get_all_images():
    image_folder = 'static'
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    images.sort()

    return images


def read_param(parametres={"HD":"off","decoupe":10,"seuil":10,"winStride":4,"padding":4,"scale":1.1,"min_blocs":5}):

    try:
        with open('./conf/param.txt', 'rb') as f:
            parametres = pickle.load(f)
    except:
        pickle.dump(parametres, open("./conf/param.txt", "wb"))
        logging.warning("pas de fichier param.txt , création par défaut")

    return parametres



@app.route('/param', methods=["GET","POST"])
def param():
    parametres={}
    if request.method == 'POST':

        try:
            parametres['HD'] = request.form['HD']
            parametres['decoupe'] = request.form['decoupe']
            parametres['seuil'] = request.form['seuil']
            parametres['winStride'] = request.form['winStride']
            parametres['padding'] = request.form['padding']
            parametres['scale'] = request.form['scale']
            parametres['min_blocs'] = request.form['min_blocs']
            logging.debug(parametres)
            pickle.dump(parametres, open("./conf/param.txt", "wb"))
        except:
            logging.warning("pas de données dans le POST param")
    return render_template('param.html',parametres=read_param(),ip=get_IP())

#TODO gestion des pages création d'onglet
@app.route('/')
def photo():
    photos = get_all_images()
    pages=(photos.__len__()//10)+1
    return render_template('photo.html',photos=photos,ip=get_IP(),pages=pages)

#TODO get_log mise en forme HTML
@app.route('/log')
def get_log(N=10):
    """
    lecture des dernières lignes
    :return: 
    """
    log_folder = 'log'
    logs = [img for img in os.listdir(log_folder)
              if img.endswith(".log") or
              img.endswith(".txt")]
    texte=''
    for i in range(0,logs.__len__()):
        with open("log/"+logs[i]) as file:
            # loop to read iterate
            # last n lines and print it
            texte+='<H1>'+logs[i]+'<BR></H1>'
            for line in (file.readlines()[-N:]):
                texte+=line+'<BR>'


    return render_template('log.html',texte=texte,ip=get_IP())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,  debug=False)