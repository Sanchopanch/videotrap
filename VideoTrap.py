import cv2
import time
from multiprocessing import Process
from compareFrames import *
import os
import pickle
from flask import Flask,render_template
import datetime as dt
from appendTimeline import appendHour

class videoTrap():
    def __init__(self):
        self.fileState = '/dev/shm/data.pickle' #in memory (Unix)
        if os.path.isfile(self.fileState):
            os.remove(self.fileState)
        pass

    def loadState(self):
        if os.path.isfile(self.fileState):
            with open(self.fileState, 'rb') as f:
                restoredDict = pickle.load(f)
        else:
            restoredDict = {}
        return restoredDict

    def saveState(self,li):
        with open(self.fileState, 'wb') as f:
            pickle.dump(li, f)

    def saveFrame(self,frame,recAll):
        #restore state
        restoredDict = self.loadState()

        scale_percent = 10
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        frameSm = cv2.resize(frame, (width, height))
        cv2.rectangle(frame, (recAll[0]-10, recAll[1]-10), (recAll[2]+10, recAll[3]+10), (150, 150, 0), 1)

        restoredDict, fName, fNameFull = appendHour(restoredDict)
        cv2.imwrite('/dev/shm/'+fName,frameSm)
        cv2.imwrite('/dev/shm/'+fNameFull,frame)


        self.saveState(restoredDict)
        # ret, buffer = cv2.imencode('.jpg', frame)
        # frame = buffer.tobytes()
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame

    def renderTimeLine(self):
        restoredDict = self.loadState()
        return render_template('timeline.html', restoredDict=restoredDict)
        # rez = ''
        # arr = os.listdir('/dev/shm')
        # for fn, tim in restoredList:
        #     rez +='<br>'+str(tim)+'<br><img src="/img/'+fn+'">'
        # return rez

    def capFrames(self):
        camera = cv2.VideoCapture(0)
        prevFrame = None
        while True:
            success, frame = camera.read()  # read the camera frame
            time.sleep(1)
            if success:
                # print("suc frame")

                if not prevFrame is None:
                    different, recs = compareFrames(prevFrame,frame.copy())
                    recAll = surroundRecs(recs)
                    if different:
                        self.saveFrame(frame,recAll)
                prevFrame = frame.copy()
                prevFrame = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)  # For converting the frame color to gray scale
                prevFrame = cv2.GaussianBlur(prevFrame, (21, 21), 0)  # For converting the gray scale frame to GaussianBlur

            else:
                # print("fail")
                break


    def beginCapture(self):
        # p = Process(target=self.beginCapture)


        p = Process(target=self.capFrames)
        p.start()
        #p.join()
        print("proc started")

# if __name__ == "__main__":
#     vt = videoTrap()
#     vt.beginCapture()