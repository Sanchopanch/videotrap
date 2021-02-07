import cv2
import time
from compareFrames import *
import os
import pickle
from flask import Flask,render_template
import datetime as dt
from appendTimeline import appendHour
import shutil
from createGIF import createGif
import asyncio

class videoTrap():
    def __init__(self):
        self.workPath = '/dev/shm/videoTrap' #in memory (linux). sorry Bill, not this time
        if os.path.isdir(self.workPath):
            shutil.rmtree(self.workPath)
        os.mkdir(self.workPath)
        self.fileState = self.workPath + '/dataState.pickle'
        self.fileTrack = self.workPath + '/dataTrack.pickle'
        pass

    # load current state if videowTrap object from shared mem
    def loadState(self):
        if os.path.isfile(self.fileState):
            with open(self.fileState, 'rb') as f:
                restoredDict = pickle.load(f)
        else:
            restoredDict = {}
        if os.path.isfile(self.fileTrack):
            with open(self.fileTrack, 'rb') as f:
                restoredList = pickle.load(f)
        else:
            restoredList = []

        return restoredDict,restoredList

    def saveState(self,di,li):
        with open(self.fileState, 'wb') as f:
            pickle.dump(di, f)
        with open(self.fileTrack, 'wb') as f:
            pickle.dump(li, f)

    def saveFrame(self,frame,recAll):

        restoredDict,restoredList = self.loadState()  #restore state
        copyFrame = frame.copy()
        tstam = time.time()
        if len(restoredList) == 0:
            restoredList.append([tstam,frame])
        else:
            lastFrame = restoredList[len(restoredList)-1]
            if tstam-lastFrame[0]<3.5 and not len(restoredList)>10:  #sec , 10 frames GIF maximum
                restoredList.append([tstam, frame])
            else:
                fGIF = createGif(restoredList)  # creating file from frames
        # cv2.rectangle(frame, (recAll[0]-10, recAll[1]-10), (recAll[2]+10, recAll[3]+10), (150, 150, 0), 1)
                frame = restoredList[int(len(restoredList)*.49)][1]
                scale_percent = 10
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                frameSm = cv2.resize(frame, (width, height))

                restoredDict, fName, fNameFull = appendHour(restoredDict, tstam, fGIF)
                cv2.imwrite(self.workPath + '/'+fName,frameSm)
                cv2.imwrite(self.workPath + '/'+fNameFull,frame)
                restoredList = []   # clear list of frames for next moove

        #save state to shared mem
        self.saveState(restoredDict,restoredList)


    def renderTimeLine(self):
        restoredDict,restoredList = self.loadState()
        return render_template('timeline.html', restoredDict = restoredDict)


    async def capFrames(self):
        camera = cv2.VideoCapture(0)
        prevFrame = None
        while True:
            success, frame = camera.read()  # read the camera frame

            if success:
                #print("suc frame")
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # For converting the frame color to gray scale
                gray = cv2.GaussianBlur(gray, (21, 21), 0)  # For converting the gray scale frame to GaussianBlur

                if not prevFrame is None:
                    different, recs = compareFrames(prevFrame,gray.copy())
                    recAll = surroundRecs(recs)
                    if different:
                        self.saveFrame(frame,recAll)
                prevFrame = gray.copy()

                await asyncio.sleep(1) #return execution for 1 sec

            else:
                #print("fail")
                await asyncio.sleep(1)





