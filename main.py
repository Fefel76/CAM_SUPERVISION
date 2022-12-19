from flask import Flask, Response
import os
import time

app = Flask(__name__)


def gen(delai=1):


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


@app.route('/slideshow')
def slideshow():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return "<html><head></head><body><h3>Capture suite à détection</h3><img src='/slideshow' style='width: 90%; height: 90%;'/>" \
           "</body></html>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)