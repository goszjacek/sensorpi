from Mode import *
import matplotlib.pyplot as plt

def init_polar_fig():
  fig = plt.figure(figsize=(8,8))
  ax = fig.add_subplot(111, projection='polar') 
  ax.set_ylim(0,400)
  return fig,ax

def polar_fig():
  fig,ax = init_polar_fig()
  l, = ax.plot([1,2,3,4,5,6,7,8,9],[50,100,150,200,250,300,350,400,450],'ro')
  return fig, l

def demo_fig(): 
  #init fig
  fig,ax = init_polar_fig()
  l, = ax.plot([],[],'ro')
  return fig, l

def rpi_fig():
  pass
  
def figureGeneratorProvider(mode):
  if(mode == Mode.DEMO):
    return demo_fig
  if(mode == Mode.STATIC):
    return polar_fig
  if(mode == Mode.RPI):
    return demo_fig