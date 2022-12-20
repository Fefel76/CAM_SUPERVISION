from flask import Flask, render_template, request, jsonify
import os
import time
import pickle

app = Flask(__name__)



def get_all_images():
    image_folder = 'static'
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    images.sort()

    return images

def read_param(parametres={"decoupe":10,"seuil":10,"winStride":4,"padding":4,"scale":1.1}):

    try:
        with open('./conf/param.txt', 'rb') as f:
            parametres = pickle.load(f)
    except:
        pickle.dump(parametres, open("./conf/param.txt", "wb"))

    return parametres



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
            print(parametres)
            pickle.dump(parametres, open("./conf/param.txt", "wb"))
        except:
            print("pas de données")
    return render_template('param.html',parametres=read_param())

@app.route('/')
def photo():
    photos = get_all_images()
    return render_template('photo.html',photos=photos)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)