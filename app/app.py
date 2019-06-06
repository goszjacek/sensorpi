



from tkinter import *
from tkinter.colorchooser import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import DataHelper
import FigureGeneratorProvider as FGP
import time
from Mode import *


data_file = 'data.json'
MODE = Mode.DEMO

# if MODE == Mode.RPI:  
from Serwo import Serwo
from Radar import Radar
mainRadar = Radar(0.1, 4, 17)
mainSerwo = Serwo(0.1, 20, 18)

animation_data = ([],0.0)



class Main(Tk):

  def __init__(self, *args, **kwargs):
      
    Tk.__init__(self, *args, **kwargs)
    container = Frame(self)

    container.pack(side="top", fill="both", expand = True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}

    self.frames[StartFrame] = StartFrame(container, self)
    self.frames[StartFrame].grid(row=0, column=0, sticky="nsew")

    self.show_frame(StartFrame)

  def show_frame(self, cont):
    frame = self.frames[cont]
    frame.tkraise()
    # frame.canvas.draw_idle()

        
class StartFrame(Frame):

  def __init__(self, parent, controller):

    #view
    Frame.__init__(self,parent)

    self.frames = {}

    topFrame = Frame(self)
    topFrame.pack()

    etykieta = Label(topFrame, text = "Configure")
    etykieta.pack()

    buttonsFrame = Frame(self)
    buttonsFrame.pack()

    self.mode_var = StringVar()
    mode_label = Entry(topFrame, text = self.mode_var, state=DISABLED)
    mode_label.pack()
    self.mode_var.set("mode : demo")



    modeButton = Button(buttonsFrame, text="Toggle", command=self.toggleMode)
    # stopButton = Button(buttonsFrame, text="Stop")

    colorChooserButton = Button(buttonsFrame,text="Choose color", command=self.chooseColor)

    buttons = [modeButton, colorChooserButton]

    for button in buttons:
      button.pack(side=LEFT)

    presenterFrame = Frame(self)
    presenterFrame.pack()

    self.presenterFrame = presenterFrame
    #endview
    

    #make things interactive
    # set_up() -> prepare arrays, data, 

    # self.canvas = getCanvas(Plot.Circle)

    # sum_up() -> draw_idle

    

    self.render(MODE)

    

      # self.anim = animation.FuncAnimation(fig, updateProvider(MODE),interval=100, fargs = rotations)
    
  def update(self,i,graphHolder):
    data,theta = DataHelper.get_points(self.rotations[i])
    graphHolder.set_data(theta, data)

  def render(self, mode):
    generator = FGP.figureGeneratorProvider(MODE)
 
    self.fig, self.graphHolder = generator()

    self.canvas = FigureCanvasTkAgg(self.fig, self.presenterFrame)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    self.setMainAnimation()


  def stopAnimation(self):
    self.anim.event_source.stop()

  def setMainAnimation(self):
    self.anim = animation.FuncAnimation(self.fig, update, interval=50,fargs=(self.graphHolder, 0))

  def setExactAnimation(self):
    if MODE == Mode.DEMO:
      rotations = DataHelper.get_rotations_from_file(data_file)    
      self.anim = animation.FuncAnimation(self.fig, updateProvider(MODE), interval=1000,fargs=(self.graphHolder, rotations))
    elif MODE == Mode.RPI:
      animation_data = ([],0.0)
      self.anim = animation.FuncAnimation(self.fig, updateProvider(MODE), interval=1000, fargs=(self.graphHolder,0))

  
    
  def updateColor(self, color):
    self.graphHolder.set_ydata([1,2,3,4,5,6,7,8])

  def chooseColor(self):
    color = askcolor()
    self.updateColor(color[0])

  def toggleMode(self):
    global MODE
    if(MODE == Mode.DEMO):
      MODE = Mode.RPI
      self.mode_var.set("mode: rpi online") 
    else:
      MODE = Mode.DEMO
      self.mode_var.set("mode: demo")


  # def rpi_update(self,i):
  #   if mainSerwo.rotation_no != self.last_rotation:
  #     self.last_rotation = mainSerwo.rotation_no
  #     self.x = []
  #     self.y = []
  #   dist = mainRadar.last_result
  #   if dist <= 430:
  #     angle = mainSerwo.get_position_in_radian()
  #     self.x.append(angle)
  #     self.y.append(dist)
  #   print(len(self.x))
  #   print(len(self.y))
  #   print("-------------------")
  #   self.set_data(x, y)
  #   print("updated")  





def update(i, graphHolder,sth):
  if(MODE == Mode.DEMO):
    rotations = DataHelper.get_rotations_from_file(data_file)    
    demo_update(i, graphHolder ,rotations)
  elif(MODE == Mode.RPI):
    online_update(i,graphHolder, 0)



def demo_update(i, graphHolder, rotations):
  if i < len(rotations):
    data,theta = DataHelper.get_points(rotations[i])
    graphHolder.set_data(theta, data)
  else:
    data,theta = DataHelper.get_points(rotations[len(rotations)-1])
    graphHolder.set_data(theta, data)




def online_update(i, graphHolder, sth):
  global animation_data
  rotation, last_angle = animation_data
  
  tmp_dist = mainRadar.last_result
  # tmp_dist = 200.0 # read dist from radar
  # if(i<10):
  #   tmp_angle = last_angle + 0.1 # read angle from sensor
  # else:
  #   tmp_angle = last_angle - 0.25
  tmp_angle = mainSerwo.get_position_in_radian()
  
  
  print(last_angle)
  print(tmp_angle)

  
  rotation = DataHelper.filterAngles(rotation, last_angle, tmp_angle)
  readout = DataHelper.create_simple_readout(tmp_angle, tmp_dist)
  
  rotation.append(readout)
  print(rotation)
  data,theta = DataHelper.get_points(rotation)
  print(theta)
  graphHolder.set_data(theta, data)
  animation_data = (rotation, tmp_angle)


def updateProvider(mode):
  if(mode == Mode.DEMO):
    return demo_update
  if(mode == Mode.RPI):
    return online_update


# def demo_frames():
#   i = 0
#   while MODE == Mode.DEMO:
#     yield i
#     i+=1

# def rpi_frames():
#   i = 0
#   while MODE == Mode.RPI:
#     yield i
#     i+=1

 

if __name__ == "__main__":

  # if(MODE == Mode.RPI):
  mainRadar.run()
  mainSerwo.run()
  time.sleep(2)
  mainRadar.stop()
  app = Main()
  app.mainloop()

