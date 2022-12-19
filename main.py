from flask import Flask, Response
import os
import time
import pickle

app = Flask(__name__)


def gen(delai=5):

    while True:

        images = get_all_images()

        for i in range(0,len(images)):
            im = open('videos/' + images[i], 'rb').read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')

            time.sleep(delai)



def get_all_images():
    image_folder = 'videos'
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    images.sort()
    return images

def read_param(decoupe=10,seuil_diff=10,winStride = (4, 4),padding = (4, 4), scale = 1.1):
    try:
        with open('./conf/decoupe.txt', 'rb') as f:
            decoupe = pickle.load(f)
    except:
        pickle.dump(decoupe, open("./conf/decoupe.txt", "wb"))

    try:
        with open('./conf/seuil_diff.txt', 'rb') as f:
            seuil_diff = pickle.load(f)
    except:
        pickle.dump(seuil_diff, open("./conf/seuil_diff.txt", "wb"))

    try:
        with open('./conf/winStride.txt', 'rb') as f:
            winStride = pickle.load(f)
    except:
        pickle.dump(winStride, open("./conf/winStride.txt", "wb"))

    try:
        with open('./conf/padding.txt', 'rb') as f:
            padding = pickle.load(f)
    except:
        pickle.dump(padding, open("./conf/padding.txt", "wb"))

    try:
        with open('./conf/scale.txt', 'rb') as f:
            scale = pickle.load(f)
    except:
        pickle.dump(scale, open("./conf/scale.txt", "wb"))

    return decoupe, seuil_diff, winStride, padding, scale

@app.route('/slideshow')
def slideshow():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    html="<html><head></head><body><h3>Capture suite à détection</h3>"
    html+="<img src=/slideshow style='width: 90%; height: 90%;'/>"
    html+="</body></html>"
    return html

@app.route('/param')
def param():
    decoupe, seuil, win, padding, scale=read_param()
    html="<html><head></head><body><h3>Paramètres pour optimiser la détection</h3><ul>"
    html+="<li> DECOUPE BLOC : "+str(decoupe)+"</li>"
    html += "<li> SEUIL BLOC : " + str(seuil) + "</li>"
    html += "<li> HOG WinStride" + str(win) + "</li>"
    html += "<li> HOG Padding" + str(padding) + "</li>"
    html += "<li> HOG Scale" + str(scale) + "</li>"
    html+="</ul></body></html>"
    return html





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)