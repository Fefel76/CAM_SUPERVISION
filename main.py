from flask import Flask, Response
import os
import time

app = Flask(__name__)


def gen():
    i = 0

    while True:
        time.sleep(1)
        images = get_all_images()
        image_name = images[i]
        im = open('videos/' + image_name, 'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')
        i += 1
        if i >= len(images):
            i = 0


def get_all_images():
    image_folder = 'videos'
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    return images


@app.route('/slideshow')
def slideshow():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return "<html><head></head><body><h1>Photos</h1><img src='/slideshow' style='width: 90%; height: 90%;'/>" \
           "</body></html>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)