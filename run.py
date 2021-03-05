#Import necessary libraries
from flask import Flask, render_template,  send_file,request,jsonify, redirect, make_response
import cv2
import time
from VideoTrap import videoTrap
from multiprocessing import Process
import os
import asyncio
from hashing import getmd5


#Initialize the Flask app
app = Flask(__name__)

lastAttempt = time.time()


@app.route('/', methods=['POST','GET'])
def index():
    global lastAttempt
    page = request.args.get('page', default=1, type=int)
    ok = False
    if 'user' not in request.cookies:
        user = request.values.get('uuu', default='figali', type=str)
        pasw = request.values.get('ppp', default='asd', type=str)
        t = user + ':' + getmd5(pasw, 2)
        print('attempt to login ' +t)
        if t == 'sasha:d7374ed42a9c0d14b9dc38e32ca86009':
            print('success! '+user)
            import random
            code = user + ':' + str(random.random())
            open('/dev/shm/videoTrap/login', 'a').write(code + '\n')
            resp = make_response(vt.renderTimeLine(page))
            resp.set_cookie('user', code)
            ok = True
    else:
        code = request.cookies['user']
        if os.path.isfile('/dev/shm/videoTrap/login'):
            for s in open('/dev/shm/videoTrap/login','r').readlines():
                if code == s.rstrip():
                    ok = True
                    resp = make_response(vt.renderTimeLine(page))
    if not ok:
        now = time.time()
        if (now - lastAttempt) < 5:
            return 'ho ho ho'
        lastAttempt = time.time()
        resp = make_response(loginForm())
        resp.delete_cookie('user')
        return resp

    # we have template for main page (timeline.html)
    return resp


@app.route('/getT', methods=['GET', 'POST'])
def getT():
    ts = request.args.get('ts', default=1000, type=float)
    return jsonify(result=vt.getLast(ts))


@app.route('/robots.txt')
def robo():
    return ' User-agent: * \n Disallow: /  '

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



def loginForm():
    return '<html><body> <form method=post >imya:<input type=text name=uuu /><br/> parol:<input type=password name=ppp /> <br /> <input type=submit /> </form> </body></html>'

if __name__ == "__main__":

    vt = videoTrap()  # this object for flask loop

    p = Process(target=createVT)
    p.start()  # starting subprocces for aditional cv2 loop

    app.run(host = '192.168.1.43',port = 5000, debug=True)