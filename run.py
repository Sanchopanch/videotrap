#Import necessary libraries
from flask import Flask, render_template, Response, send_file,request,jsonify
import cv2
import time
from VideoTrap import videoTrap
from multiprocessing import Process
import os
import asyncio


#Initialize the Flask app
app = Flask(__name__)



@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    # we have template for main page (timeline.html)
    return vt.renderTimeLine(page)

@app.route('/getT', methods=['GET', 'POST'])
def getT():
    ts = request.args.get('ts', default=1000, type=float)
    return jsonify(result=vt.getLast(ts))



@app.route('/img/<name>')
def imgRender(name):
    # static pictures to send
    arr = os.listdir('/dev/shm/videoTrap')
    if name in arr:
        return send_file('/dev/shm/videoTrap/'+name, mimetype='image/jpg')

def createVT():
    # we are in subprocess
    vtCV2 = videoTrap() # this object for cv2 loop
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(vtCV2.capFrames())
    ioloop.close()
    print('loop closed :(')

if __name__ == "__main__":

    vt = videoTrap()  # this object for flask loop

    p = Process(target=createVT)
    p.start()  # starting subprocces for aditional cv2 loop

    app.run(host = '192.168.1.43',port = 5000, debug=True)