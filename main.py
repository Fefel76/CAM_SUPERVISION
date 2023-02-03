from flask import Flask, render_template, request, jsonify
import os
import time
import logging
import pickle
import socket
from datetime import datetime


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


def read_param(name,parametres={"HD":"off","decoupe":10,"seuil":10,"winStride":4,"padding":4,"scale":1.1,"min_blocs":5}):

    try:
        filename='./conf/param_'+name+'.txt'
        with open(filename, 'rb') as f:
            parametres = pickle.load(f)
    except:
        pickle.dump(parametres, open(filename, "wb"))
        logging.warning("pas de fichier param.txt , création par défaut")

    return parametres



@app.route('/param/<name>', methods=["GET","POST"])
def param(name):
    parametres={}
    if request.method == 'POST':
        print("name:",name)


        try:
            parametres['HD'] = request.form['HD']
            parametres['decoupe'] = request.form['decoupe']
            parametres['seuil'] = request.form['seuil']
            parametres['winStride'] = request.form['winStride']
            parametres['padding'] = request.form['padding']
            parametres['scale'] = request.form['scale']
            parametres['min_blocs'] = request.form['min_blocs']
            logging.debug(parametres)
            filename='./conf/param_'+name+'.txt'
            pickle.dump(parametres, open(filename, "wb"))
        except:
            logging.warning("pas de données dans le POST param")
    return render_template('param.html',parametres=read_param(name=name),ip=get_IP(),name=name)

#TODO gestion des pages création d'onglet
@app.route('/')
def photo():
    photos = get_all_images()
    pages=(photos.__len__()//10)+1
    return render_template('photo.html',photos=photos,ip=get_IP(),pages=pages)


@app.route('/log', methods=["GET","POST"])
def get_log(N=10):
    """
    lecture des dernières lignes
    :return: 
    """
    if request.method == 'POST':
        N = int(request.form['N'])

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


    return render_template('log.html',texte=texte,ip=get_IP(), N=N)

@app.route('/purge', methods=["GET","POST"])
def purge():
    texte=''
    rep='static/'
    t=datetime.now()
    if request.method == 'POST':
        d= request.form['d']
        d=datetime.strptime(d, '%Y-%m-%d')

        # récupération de la liste des images disponibles
        images=get_all_images()

        for im in images:
            t=time.ctime(os.path.getctime(rep+im))
            t=datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
            if t<d:
                texte+="fichier <B> {} </B>supprimé <BR>".format(im)
                logging.info("Fichier {} supprimé".format(im))

                try:
                    os.remove(rep+im)
                except:
                    logging.error("Erreur lors de la suppression du fichier {} ".format(im))


    return render_template('purge.html', ip=get_IP(), d=t.strftime("%Y-%m-%d"), texte=texte)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,  debug=True)