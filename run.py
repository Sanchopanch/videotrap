#Import necessary libraries
from flask import Flask, render_template, Response, send_file
import cv2
import time
from VideoTrap import videoTrap
from multiprocessing import Process
import os
#Initialize the Flask app
app = Flask(__name__)



@app.route('/')
def index():
    return vt.renderTimeLine()
    # return render_template('fl.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(vt.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/img/<name>')
def imgRender(name):
    arr = os.listdir('/dev/shm')
    if name in arr:
        return send_file('/dev/shm/'+name, mimetype='image/jpg')
        # frame = cv2.imread('/dev/shm/'+name)
        # ret, buffer = cv2.imencode('.jpg', frame)
        # frame = buffer.tobytes()
        # return b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame

if __name__ == "__main__":
    vt = videoTrap()
    p = Process(target=vt.capFrames)
    p.start()
    # p.join()
    print("proc started")
    # vt.beginCapture()
    #app.logger.setLevel(logging.CRITICAL)
    app.run(host = '192.168.1.98',port = 5000, debug=False)