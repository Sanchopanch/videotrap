import cv2

def compareFrames(frame1,frame2, tolerance = 150):
#    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)  # For converting the frame color to gray scale
#    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # For converting the gray scale frame to GaussianBlur
    delta_frame = cv2.absdiff(frame1, frame2)  # calculates the difference between first and other frames
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
    # Provides threshold value, so if the difference is <30 it will turn to black otherwise if >30 pixels will turn to white
    cnts, hrr = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)  # Define the contour area,i.e. adding borders
    currentRecs = []
    # Removing noises and shadows, any part which is greater than 1000 pixels will be converted to white
    for contour in cnts:
        if cv2.contourArea(contour) < tolerance:
            continue
        status = 1  # change in status when the object is detected
        # Creating a rectangular box around the object in frame
        (x, y, w, h) = cv2.boundingRect(contour)
        currentRecs.append([x, y, x + w, y + h])
    #    cv2.rectangle(frameR, (x, y), (x + w, y + h), (150, 150, 0), 1)
    if len(currentRecs)>0:
        return True,currentRecs
    else:
        return False,[]
def surroundRecs(recs):
    minx,miny,maxx,maxy = 9999,9999,0,0
    for rec in recs:
        minx = rec[0] if minx > rec[0] else minx
        miny = rec[1] if miny > rec[1] else miny
        maxx = rec[2] if maxx < rec[2] else maxx
        maxy = rec[3] if maxy < rec[3] else maxy

    return  [minx,miny,maxx,maxy]