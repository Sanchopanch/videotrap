import time
import datetime as dt
from sortingDict import ordDic

def appendHour(restoredDict):
    dni = ['понедельник','вторник','среда','четверг','пятница','суббота','воскресенье']
    mes = ['ee','янв','фев','мар','апр','мая','июн','июл','авг','сен','окт','ноя','дек']
    vrem = time.time()
    fName = str(vrem) + 't.jpg'
    fNameFull = str(vrem) + '.jpg'
    curr = dt.datetime.fromtimestamp(vrem)
    currD = '%s.%s.%s' % (str(curr.day).zfill(2), mes[curr.month], dni[curr.weekday()])  #   '04.фев.четверг'
    currH = '%s:00' % (str(curr.hour).zfill(2))
##    print('curD', currD)
##    print('currH', currH)
    if not currD in restoredDict:
        restoredDict[currD] = {currH : [[fName, fNameFull, time.time()]]}
        restoredDict = ordDic(restoredDict)
    else:
        if not currH in restoredDict[currD]:
            restoredDict[currD][currH] = [[fName, fNameFull, time.time()]]
            restoredDict[currD] = ordDic(restoredDict[currD])
        else:
            restoredDict[currD][currH].insert(0,[fName, fNameFull, time.time()])

    # restoredList.append([currD,[currH,[fName,fNameFull,time.time()]]])

    return restoredDict, fName, fNameFull


if __name__ == "__main__":
    a = {}
    a,_,_ = appendHour(a)
    time.sleep(1)
    a,_,_ = appendHour(a)
    print(a)