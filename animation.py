import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
 
def f(a):
    return a +np.random.random()
 
 
class AnimaPlot(object):
    def __init__(self,ax,data_lengh=200):
        self.data = 0
        self.data_lengh = data_lengh
        self.line, = ax.plot([], [], '.-r')
        self.x = []
        self.y = []


        self.ax = ax

        
        self.ax.set_xlim(0, 21)
        self.ax.set_ylim(0, 21)
        self.ax.grid(True)
        # self.ax.axvline(prob, linestyle='--', color='black')
 
    def init(self):

        self.ax.axvline(self.data, linestyle=':', color='black')
        self.line.set_data([], [])
        return self.line,
 
    def __call__(self, i):

        if i == 0:
            return self.init()
 

        if len(self.x) >self.data_lengh:
            del(self.x[0])
        if len(self.y)> self.data_lengh:
            del(self.y[0])

        self.x.append(self.data)
        self.x_=self.data
        self.y_=self.data
        self.data = f(self.data)
        self.y.append(f(self.data))
        self.line.set_data(self.x, self.y)
        self.ax.set_xlim(self.data-50, self.data)
        self.ax.set_ylim(self.data-50, self.data)
        return self.line,
 


 
 

#frames
fig, ax = plt.subplots()

ap = AnimaPlot(ax)
_ = FuncAnimation(fig, ap, frames=100, init_func=ap.init,
                     interval=100, blit=False)

plt.show()


#frames  帧 设定帧长度
#blit 动态移动坐标。为True时坐标固定
#interval 更新间隔：单位毫秒
#self.x和self.y设置成数值，为坐标的点
#
