import os
import imageio, numpy as np
import cv2
import time,datetime

def createGif(restoredList):
    now = datetime.datetime.now()
    timestr = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
    lavY,valX,_ = restoredList[0][1].shape
    timeStart = time.time()
    try:
        os.mkdir('/dev/shm/videoTrap/' + timestr)
    except:
        return
    filePics = []
    for i,cadr in enumerate(restoredList):
        frame = cadr[1]
        scale_percent = 10
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        frameSm = cv2.resize(frame, (width, height))
        fileName = '/dev/shm/videoTrap/' + timestr + '/' + str('{:04}'.format(i)) + '.jpg'
        cv2.imwrite(fileName, frameSm)  #[y1:y2, x1:x2])
        filePics.append(fileName)
    nameGIF = '/dev/shm/videoTrap/'+timestr+'.gif'
    with imageio.get_writer(nameGIF, mode='I',fps=2) as writer:
        for filename in filePics:
            image = imageio.imread(filename)
            writer.append_data(image)

    for filename in filePics:
        os.remove(filename)
    os.rmdir('/dev/shm/videoTrap/' + timestr)
    dtim = (-timeStart + time.time())
    print(timestr + " kadrs="+str(len(restoredList))+" time="+str(dtim))
    return timestr+'.gif'

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    #success, frame = camera.read()

    restoredList = []

    time.sleep(2)

    for i in range(5):
        _, frame1 = camera.read()
        tim = time.time()
        restoredList.append([tim,frame1.copy()])
        print("saved %i frame , %f"%(i,tim))
        time.sleep(1)
    createGif(restoredList)


