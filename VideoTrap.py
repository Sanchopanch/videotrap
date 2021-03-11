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
from w import getweather,getDescWind
import time

class videoTrap():
    def __init__(self):
        self.workPath = '/dev/shm/videoTrap' #in memory (linux). sorry Bill, not this time
        if os.path.isdir(self.workPath):
            shutil.rmtree(self.workPath)
        os.mkdir(self.workPath)
        self.fileState = self.workPath + '/dataState.pickle'
        self.fileTrack = self.workPath + '/dataTrack.pickle'
        self.scale_percent = 20
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

    def saveFrame(self,frame,recAll, timeout = False):

        restoredDict,restoredList = self.loadState()  #restore state
        #copyFrame = frame.copy()
        tstam = time.time()
#        if len(restoredList) == 0:
        restoredList.append([tstam,frame])
        lastFrame = restoredList[len(restoredList)-1]
        if tstam-lastFrame[0]<3.5 and not len(restoredList)>10 and not timeout:  #sec , 10 frames GIF maximum
            pass
        else:
            fGIF = createGif(restoredList, self.workPath,self.scale_percent)  # creating file from frames
            frameM = restoredList[int(len(restoredList)*.49)][1]
            width = int(frameM.shape[1] * self.scale_percent / 100)
            height = int(frameM.shape[0] * self.scale_percent / 100)
            frameSm = cv2.resize(frameM, (width, height))
            if not recAll is None:
                cv2.rectangle(frameM, (recAll[0]-10, recAll[1]-10), (recAll[2]+10, recAll[3]+10), (150, 150, 0), 1)

            restoredDict, fName, fNameFull = appendHour(restoredDict, tstam, fGIF)
            cv2.imwrite(self.workPath + '/'+fName,frameSm)
            cv2.imwrite(self.workPath + '/'+fNameFull,frameM)
            tstam = time.time() #again
            restoredList = [[tstam,frame]]   # clear list of frames for next moove

            #delete oldy frames from mem
            if len(restoredDict)>0:
                firstDate = list(restoredDict.keys())[-1]
                if len(restoredDict[firstDate])>0:
                    firstHour = list(restoredDict[firstDate].keys())[-1]
                    firstTS = restoredDict[firstDate][firstHour][0][3]
                    if tstam - firstTS > 86400 * 1:   #* days
                        print('deleting '+firstDate)
                        for hhh,lis in restoredDict[firstDate].items():
                            for kkk in lis:
                                os.remove(self.workPath + '/'+kkk[0])
                                os.remove(self.workPath + '/'+kkk[1])
                                os.remove(self.workPath + '/'+kkk[2])
                        del restoredDict[firstDate]



        #save state to shared mem
        self.saveState(restoredDict,restoredList)


    def renderTimeLine(self,page):
        restoredDict,restoredList = self.loadState()
        days = list(restoredDict.keys())
        LastDay, lastHour ='',''
        if len(days)>0:
            LastDay  = days[0]
            lastHour = list(restoredDict[LastDay].keys())[0]

        data = getweather(1486209)
        if data is None:
            data = {'main':{'temp':'-','pressure':0},'weather':[{'description':'--'}],'wind':{'speed':'-','deg':0},'name':'Ekat'}
        t = str(data['main']['temp'])+'°'
        con = data['weather'][0]['description']
        wind = str(data['wind']['speed'])+' m/s, '
        winddeg = data['wind']['deg']
        winddesc = getDescWind(winddeg)
        place = data['name']
        pressure = data['main']['pressure']

        weather = {'t':t,'con':con,'wind':wind,'winddesc':winddesc,'place':place,'pressure':pressure}

        if page==1:
            coun = 0
            for ddd,dic in restoredDict.items():
                for hhh, lis in dic.items():
                    i = 0
                    while i<len(lis):
                        coun += 1
                        if coun > 30:
                            del lis[i]
                        else:
                            i += 1

                    restoredDict[ddd][hhh]=lis
        return render_template('timeline.html',
                               restoredDict = restoredDict
                               ,LastDay = LastDay
                               ,lastHour = lastHour
                               ,weather = weather
                               , page = page
                               ,currTS = time.time())

    def getLast(self,ts):
        restoredDict,restoredList = self.loadState()
        rezList = []
        for ddd, dic in restoredDict.items():
            for hhh, lis in dic.items():
                for frame in lis:
                    if ts < frame[3]:
                        curr = dt.datetime.fromtimestamp(frame[3])
                        currH = '%s:00' % (str(curr.hour).zfill(2))
                        frame.append(currH)
                        rezList.append(frame)
        result = {'currTS':time.time(),'len':len(rezList)}
        rezList = sorted(rezList, key=lambda x: x[3], reverse=False)
        if len(rezList)>0:
            result['rez'] = rezList
        return result
        pass

    async def capFrames(self):
        tolerance = 2 #cadrs
        lastC = 0 #cadrs
        camera = cv2.VideoCapture(-1)
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
                        lastC = 1
                    elif lastC>0:
                        if lastC <= tolerance:
                            lastC +=1
                            self.saveFrame(frame, None)
                        else:
                            lastC = 0
                            self.saveFrame(frame, None, timeout=True)

                prevFrame = gray.copy()

                await asyncio.sleep(1) #return execution for 1 sec

            else:
                #print("fail")
                await asyncio.sleep(0.4)





