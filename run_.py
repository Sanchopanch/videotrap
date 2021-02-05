import cv2
from datetime import datetime
import math,random, os
import time
import imageio
from PIL import Image

from multiprocessing import Process, Pipe, Lock

def createFilmMP(loc,connec):#,vid,numF):
    print('Starting video process')
    while True:
        estCho=connec.poll(timeout=1)
        if not estCho:
            print("child:nothing")
            continue
        print("some thing")
        task = connec.recv()
        vid,numF = task
        if len(vid.cadrs)<vid.maxTolerance*2:
            continue
        timestr = now.strftime("%Y-%m-%d-%H-%M-%S-%f")+'--'+str(numF)+'k'+str(len(vid.cadrs))
        try:
            os.mkdir('pics/'+timestr)
        except:
            continue
        timeStart = time.time()
        filePics=[]
        for i,cadr in enumerate(vid.cadrs):
            rad = vid.circles[i]
            x,y = vid.coords[i]
            fileName = 'pics/'+timestr+'/'+str('{:04}'.format(i))+'.png'
            x1 = int(vid.coords[i][0]-vid.radius)
            x2 = int(vid.coords[i][0]+vid.radius)
            y1 = int(vid.coords[i][1]-vid.radius)
            y2 = int(vid.coords[i][1]+vid.radius)
            x1,x2 = (0,x2-x1) if x1<0 else (x1,x2)
            x2,x1 = (len(cadr[0])-1,x1-(x2-len(cadr[0])-1)) if x2>len(cadr[0])-1 else (x2,x1)
            y1,y2 = (0,y2-y1) if y1<0 else (y1,y2)
            y2,y1 = (len(cadr)-1,y1-(y2-len(cadr)-1)) if y2>len(cadr)-1 else (y2,y1)
            if x1<0 or x2>len(cadr[0])-1 or y1<0 or y2>len(cadr):
                continue
            cv2.imwrite(fileName, cadr[y1:y2, x1:x2])
            filePics.append(fileName)
        with imageio.get_writer('pics/'+timestr+'.gif', mode='I',fps=6) as writer:
            for filename in filePics:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in filePics:
            os.remove(filename)
        os.rmdir('pics/'+timestr)
        dtim=(-timeStart+time.time())        
        print(timestr+" kadrs. rad="+str(vid.radius)+" x="+str(vid.currX)+" y="+str(vid.currY)+" time="+str(dtim))


class vido():
    def __init__(self,currX,currY,radius):
        self.cadrs = []
        self.times = []
        self.rects = []
        self.circles = [int(radius)]
        self.coords = [(int(currX),int(currY))]
        self.vX = 0
        self.vY = 0
        self.currX = int(currX)
        self.currY = int(currY)
        self.minRad = 150
        self.radius = int(max(self.minRad, radius))
        self.maxTolerance = 8
        self.tolerance = self.maxTolerance
        self.col = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def calc(self):
        if len(self.rects)==0:
            return
        x,y,rad = 0,0,0
        
        for rec in self.rects:
            x+= (rec[0]+rec[2])/2
            y+= (rec[1]+rec[3])/2
            rad+=(rec[0]-rec[2]+rec[1]-rec[3])/2
        x   = x   / len(self.rects)
        y   = y   / len(self.rects)
        rad = max(self.minRad, rad / len(self.rects))
        self.vX = (-self.currX+x + self.vX)/2
        self.vY = (-self.currY+y + self.vY)/2
        self.radius = (rad + self.radius)/2
        self.currX = int((x+self.currX+self.vX)/2)
        self.currY = int((y+self.currY+self.vY)/2)
        self.coords.append((self.currX,self.currY))
        self.circles.append(int(self.radius))
        self.rects.clear()

    def createFilm(self,numF):
        if len(self.cadrs)<self.maxTolerance*2:
            return
        timestr = now.strftime("%Y-%m-%d-%H-%M-%S-%f")+'--'+str(numF)+'k'+str(len(self.cadrs))
        try:
            os.mkdir('pics/'+timestr)
        except:
            return
        timeStart = time.time()
        filePics=[]
        for i,cadr in enumerate(self.cadrs):
            rad = self.circles[i]
            x,y = self.coords[i]
            fileName = 'pics/'+timestr+'/'+str('{:04}'.format(i))+'.jpg'
            x1 = int(self.coords[i][0]-self.radius)
            x2 = int(self.coords[i][0]+self.radius)
            y1 = int(self.coords[i][1]-self.radius)
            y2 = int(self.coords[i][1]+self.radius)
            x1,x2 = (0,x2-x1) if x1<0 else (x1,x2)
            x2,x1 = (len(cadr[0])-1,x1-(x2-len(cadr[0])-1)) if x2>len(cadr[0])-1 else (x2,x1)
            y1,y2 = (0,y2-y1) if y1<0 else (y1,y2)
            y2,y1 = (len(cadr)-1,y1-(y2-len(cadr)-1)) if y2>len(cadr)-1 else (y2,y1)
            if x1<0 or x2>len(cadr[0])-1 or y1<0 or y2>len(cadr):
                return
##            print(str(i)+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' ') 
            cv2.imwrite(fileName, cadr[y1:y2, x1:x2])
            filePics.append(fileName)
        with imageio.get_writer('pics/'+timestr+'.gif', mode='I',fps=6) as writer:
            for filename in filePics:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in filePics:
            os.remove(filename)
        os.rmdir('pics/'+timestr)
        dtim=(-timeStart+time.time())        
        print(timestr+" kadrs. rad="+str(self.radius)+" x="+str(self.currX)+" y="+str(self.currY)+" time="+str(dtim))
                
if __name__ == '__main__':
    lock=Lock()
    parent_conn, child_conn = Pipe()
    p = Process(target=createFilmMP, args=(lock,child_conn))
    p.start()
    print("proc started")


    prev_frame = None
    timeToCompare = 5
    video = cv2.VideoCapture(0,cv2.CAP_DSHOW) 
##    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
##    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    check,frame = video.read()
    key = cv2.waitKey(2000)
    currVideos = []
    
    while True:
        check,frame = video.read()
        if not check:
            print("no video yet")
            continue
        frameR = frame.copy()
        status = 0
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  # For converting the frame color to gray scale
        gray = cv2.GaussianBlur(gray,(21,21),0)  # For converting the gray scale frame to GaussianBlur

        if prev_frame is None:
            prev_frame = gray   # used to store the first image/frame of the video
            continue

        delta_frame = cv2.absdiff(prev_frame,gray)#calculates the difference between first and other frames
        thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
        thresh_delta = cv2.dilate(thresh_delta,None,iterations=0) #Provides threshold value, so if the difference is <30 it will turn to black otherwise if >30 pixels will turn to white
        cnts,hrr = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Define the contour area,i.e. adding borders
        currentRecs = []
        #Removing noises and shadows, any part which is greater than 1000 pixels will be converted to white
        for contour in cnts:
            if cv2.contourArea(contour) < 150:
                continue
            status = 1 #change in status when the object is detected
            #Creating a rectangular box around the object in frame
            (x,y,w,h) = cv2.boundingRect(contour)
            currentRecs.append([x,y,x+w,y+h])
            cv2.rectangle(frameR,(x,y),(x+w,y+h),(150,150,0),1)

        ##*******************************************************************************************    
        if not prev_frame is None and status==1:
            now = datetime.now()
            for rec in currentRecs:
                attached = False
                for vid in currVideos:
                    dist = math.sqrt( ((rec[0]+rec[2])/2 - vid.currX)**2 +((rec[1]+rec[3])/2- vid.currY)**2 )
                    if dist <= vid.radius:
                        vid.rects.append(rec.copy())
                        attached = True

                if not  attached:
                    newVideo = vido((rec[0]+rec[2])/2, (rec[1]+rec[3])/2, (rec[2]-rec[0]+rec[3]-rec[1])/2)
                    newVideo.rects.append(rec.copy())
                    currVideos.append(newVideo)
                    
                  
        for i in reversed(range(len(currVideos))):
            vid = currVideos[i]
            if len(vid.rects)==0:
                if vid.tolerance==0:
                    timeStart = time.time()
##                    vid.createFilm(i)
##                    print("sending to child")
                    parent_conn.send((vid,i))
##                    createFilmMP(vid,i)
                    dtim=(-timeStart+time.time())        
##                    print(" time="+str(dtim))

                    del currVideos[i]
                else:
                    vid.tolerance -= 1 
                    vid.cadrs.append( frame.copy())  
                    vid.times.append( now)
                    vid.currX = int(vid.coords[len(vid.coords)-1][0]+vid.vX)
                    vid.currY = int(vid.coords[len(vid.coords)-1][1]+vid.vY)
                    vid.coords.append((int(vid.currX),int(vid.currY)))
                    vid.circles.append(int(vid.radius))
                    
            else:
                vid.calc()
                vid.cadrs.append( frame.copy())  
                vid.times.append( now)
                vid.tolerance = vid.maxTolerance
                        
        for vid in currVideos:
            for i,coord in enumerate(vid.coords):
                if i>0:
                    cv2.line(frameR, coord, vid.coords[i-1], vid.col,1)
            cv2.circle(frameR, (vid.currX,vid.currY), int(vid.radius), vid.col,1)

        cv2.imshow('cam',frameR)
        if timeToCompare==0:
            prev_frame = gray.copy()
            timeToCompare = 5
        else:
            timeToCompare -= 1        
        key = cv2.waitKey(100)

        #Used for terminating the loop once 'q' is pressed
        if key == ord('q'):
            break



    video.release()
    cv2.destroyAllWindows #will be closing all the windows
