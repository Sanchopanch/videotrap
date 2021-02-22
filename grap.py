import matplotlib.pyplot as plt
import numpy as np
import os

def getPlot(x,y,y2):
    fig, ax = plt.subplots()
    myhex = '#FFFFAA'
    ax.plot(x, y, color=myhex)
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.tick_params(colors='gray')
    plt.ylabel('Temp C°',color='gray')
    plt.grid(True,color = '#333333',linestyle = '--')

    ax2 = ax.twinx()
    ax2.plot(x, y2, color='#660000')
    ax2.set_ylabel('Pressure', color='#FF0000')
    ax2.tick_params('y', colors='#FF0000')
    fig.set_size_inches(8, 3)

    #plt.show()

    workPath = '/dev/shm/foreca'
    if not os.path.isdir(workPath):
        os.mkdir(workPath)

    plt.savefig(workPath+'/weath.png')

if __name__ == "__main__":

    x = ['19:00','21:00','23:00','01:00','03:00']
    y = [-17,-18,-15,-11,-10]
    y2 = [1020,1040,1055,1002,980]
    getPlot(x,y,y2)
