from flask import Flask, render_template, Response, request
import cv2
from time import sleep
import mmap
import numpy as np

mm = mmap.mmap(-1, 2)

app = Flask(__name__)

video_list = [{"path": "./videos/vid1.mp4", "bname": "sbs"},
              {"path": "./videos/vid2.mp4", "bname": "kbs"}]

@app.route('/')
def index():
    mm.seek(0)
    mm.write(b'FF')
    return render_template('index.html')


def gen(video_id):
    # file_path = './videos/vid1.mp4'
    file_path = video_list[video_id]["path"]
    bname = video_list[video_id]["bname"]
    print("gen", video_id, file_path, bname)

    vid = cv2.VideoCapture(file_path)

    print(chr(mm[video_id]))

    while chr(mm[video_id]) == 'F':
        frame = np.zeros([360,720,3],dtype=np.uint8)
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        sleep(1)

    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break

        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

        sleep(0.02)

    vid.release()


@app.route('/video_feed/<int:video_id>')
def video_feed(video_id):
    print("video_feed {}".format(video_id))
    return Response(gen(video_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/form', methods=['POST'])
def form():
    video_id = request.form['video_id']
    video_id = int(video_id)
    print("form", video_id)
    mm.seek(video_id)
    mm.write(b'T')
    return "Done"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
