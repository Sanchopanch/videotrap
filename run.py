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


@app.route('/img/<name>')
def imgRender(name):
    arr = os.listdir('/dev/shm/videoTrap')
    if name in arr:
        return send_file('/dev/shm/videoTrap/'+name, mimetype='image/jpg')


if __name__ == "__main__":
    vt = videoTrap()
    p = Process(target=vt.capFrames)
    p.start()
    print("proc started")

    app.run(host = '192.168.1.98',port = 5000, debug=False)