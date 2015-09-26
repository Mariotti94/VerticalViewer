from Tkinter import *
from tkMessageBox import *
import ttk,tkFileDialog
import glob
from PIL import Image, ImageTk
import os

import platform
usedos = platform.system()


def init():
      global canvas,b1,menucanvas,bottommenu,var
      menucanvas = Canvas(frame)
      btn_load = Button(menucanvas, text="Load", width=10, command=SelectLoadType)
      btn_load.pack(side=LEFT,padx=5)

      var = StringVar(root)
      var.set("1 image") 
      option = OptionMenu(menucanvas, var, "1 image", "10 images")
      option.pack(side=LEFT)

      menucanvas.pack(side=TOP,anchor=W)
      canvas = Canvas(frame)
      canvas.pack(expand=YES,fill=BOTH)
      bottommenu = Canvas(frame,height=10)
      global buttonmenu
      buttonmenu = Frame(bottommenu)
      buttonmenu.pack()
      bottommenu.pack(expand=YES,fill=BOTH)
      
def SelectLoadType():
      global var
      if var.get() == "1 image":
        LoadImage()
      if var.get() == "10 images":
        LoadFolder()


def destroywin():
      for widget in frame.winfo_children():
        widget.destroy()

def LoadFolder():
      global index
      global photo
      global photolist
      global filenames
      global factor,scalevalue
 
      scalevalue=100
      dirname=""
      photolist = []
      filenames = []
      filetypes = ['*.jpg','*.png','*.gif','*.bmp']

      dirname=tkFileDialog.askdirectory(title='Select a directory')
      dirname=dirname.replace("\\","/")
      dirname=dirname.replace("[","\[")
      dirname=dirname.replace("]","\]")
      dirname=dirname.replace("\[","[[]")
      dirname=dirname.replace("\]","[]]")
      if dirname=="":
          showwarning("Load Error","You haven't selected a folder")
      else:
          for type in filetypes:
                files = glob.glob(dirname+"//"+type)
                for name in files:
                          name=name.replace("\\","/")
                          filenames.append(name)
          index = 0
          factor = 1
          NextTen()

def NextTen():
      global index
      global maxheight,sumheight,imagesheight
      global maxwidth,imageswidth
      global photo
      global photolist
      global filenames
      global i
      global factor,scalevalue

      destroywin()
      init()
      canvas.pack_forget()
      maxwidth = 0
      maxheight = 0
      sumheight = 0
      
      imageswidth=[]
      imagesheight=[]

      buttonmenu.pack_forget()


      if (len(filenames)-index) > 10:
          
          bottommenu.pack_forget()
          global next_btn
          next_btn = Button(buttonmenu, text="Next", width=15, command=NextTen)
          next_btn.pack(side=RIGHT)
          root.bind('<Right>', RightKeypressFolder)
          bottommenu.pack(side=BOTTOM)

          for i in range(10):
                string = filenames[index]
                im = Image.open(string)
                photo = ImageTk.PhotoImage(im)
                
                imageswidth.append(photo.width())
                imagesheight.append(photo.height())

                if photo.width()>maxwidth:
		            maxwidth=photo.width()
    	        if photo.height()>maxheight:
		            maxheight=photo.height()
                index = index + 1

          index=index-(i+1)
                   
          for i in range(10):
                
                string = filenames[index]
                im = Image.open(string)
                
                im = im.resize((int(imageswidth[i]*factor),int(imagesheight[i]*factor)), Image.ANTIALIAS)

                photo = ImageTk.PhotoImage(im)
                photolist.append(photo)
                canvas.create_image(10+(maxwidth*factor-photo.width())/2,10+(sumheight+20*i),anchor=NW, image=photo)
                sumheight = sumheight + photo.height()
                index = index + 1
                
      else:
          root.bind('<Right>', ignore)
          
          for i in range(len(filenames)-index):
                
                string = filenames[index]
                im = Image.open(string)
                photo = ImageTk.PhotoImage(im)
                
                imageswidth.append(photo.width())
                imagesheight.append(photo.height())

                if photo.width()>maxwidth:
		            maxwidth=photo.width()
            	if photo.height()>maxheight:
        		    maxheight=photo.height()
                index = index + 1

          index=index-(i+1)

          for i in range(len(filenames)-index):
                string = filenames[index]
                im = Image.open(string)
                
                im = im.resize((int(imageswidth[i]*factor),int(imagesheight[i]*factor)), Image.ANTIALIAS)

                photo = ImageTk.PhotoImage(im)
                photolist.append(photo)
                canvas.create_image(10+(maxwidth*factor-photo.width())/2,10+(sumheight+20*i),anchor=NW, image=photo)
                sumheight = sumheight + photo.height()
                index= index+1
                
      if (index - 10) > 0:
          bottommenu.pack_forget()
          global previous_btn
          previous_btn = Button(buttonmenu, text="Previous", width=15, command=PreviousTen)
          previous_btn.pack(side=LEFT)
          root.bind('<Left>', LeftKeypressFolder)
          bottommenu.pack(side=BOTTOM)
      else:
          root.bind('<Left>',ignore)

      buttonmenu.pack(side=LEFT,fill=Y,padx=50)

      bottommenu.pack_forget()
      global zoommenu
      zoommenu = Frame(bottommenu)

      reset_zoom_btn = Button(zoommenu, text="Reset", command=ResetScale)
      reset_zoom_btn.pack(side=LEFT)
      global zoomscale
      zoomscale = Scale(zoommenu, from_=10, to=200, orient=HORIZONTAL)
      zoomscale.set(scalevalue)
      zoomscale.pack(side=LEFT)
      global zoom_btn
      zoom_btn = Button(zoommenu, text="Zoom", width=10, command=ScaleFolder)
      zoom_btn.pack(side=RIGHT)

      zoommenu.pack(anchor=E,padx=20,side=RIGHT)
      bottommenu.pack(side=BOTTOM,fill=BOTH,expand=NO)

      canvas.configure(width=maxwidth*factor+20,height=maxheight*factor+20)
      canvas.configure(scrollregion=(0,0,maxwidth*factor+20,sumheight+20*(i+1)))
      canvas.place(relx=0.5,rely=0.5,anchor=CENTER)

      hbar=Scrollbar(frame,orient=HORIZONTAL)
      hbar.pack(side=BOTTOM,fill=X)
      hbar.config(command=canvas.xview)
      vbar=Scrollbar(frame,orient=VERTICAL)
      vbar.pack(side=RIGHT,fill=Y)
      vbar.config(command=canvas.yview)
      canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
      frame.pack(expand=YES,fill=BOTH)
      canvas.pack(expand=YES, fill=Y)
      if usedos == 'Windows':
         root.bind("<MouseWheel>", mouse_wheel)
      else:
         root.bind("<Button-4>", mouse_wheel)
         root.bind("<Button-5>", mouse_wheel)
      root.bind('<Up>',ScrollUp)
      root.bind('<Down>',ScrollDown)

def PreviousTen():
      global index
      global i

      index=index-(i+1)-10
      NextTen()

def ScaleFolder():
      global factor
      global zoomscale
      global index
      global i,scalevalue

      scalevalue = zoomscale.get()
      factor= zoomscale.get()*0.01 
      index=index-(i+1)
      NextTen()


def LoadImage():
      global index
      global photo
      global filenames
      global im
      global factor,scalevalue

      global imagewidth
      global imageheight
      
      openedimage=""
      scalevalue=100

      photolist = []
      filenames = []
      filetypes = ['*.jpg','*.png','*.gif','*.bmp']
      position_list = 0      

      openedimage=tkFileDialog.askopenfilename(title='Select an image',filetypes=[('JPG','*.jpg'),('PNG','*.png'),('BMP','*.bmp'),('GIF','*.gif')])

      if openedimage=="":
          showwarning("Load Error","You haven't selected an image")
      else:
          imagedir= os.path.dirname(os.path.abspath(openedimage))
          imagedir=imagedir.replace("\\","/")
          imagedir=imagedir.replace("[","\[")
          imagedir=imagedir.replace("]","\]")
          imagedir=imagedir.replace("\[","[[]")
          imagedir=imagedir.replace("\]","[]]")
          for type in filetypes:
                files = glob.glob(imagedir+"/"+type)
                for i in range(len(files)):
                          files[i]=files[i].replace("\\","/")
                          filenames.append(files[i])
                          if files[i] == openedimage:
                                    index=position_list
                          position_list = position_list + 1

          index = index - 1
          factor = 1
          NextImage()


def NextImage():
      global index
      global photo
      global filenames
      global im
      global scalevalue

      global imagewidth
      global imageheight

      index = index + 1
      destroywin()
      init()
      canvas.pack_forget()

      global buttonmenu
      buttonmenu = Frame(bottommenu)

      if index != 0:
          bottommenu.pack_forget()
          global previous_btn
          previous_btn = Button(buttonmenu, text="Previous", width=15, command=PreviousImage)
          previous_btn.pack(side=LEFT)
          root.bind('<Left>', LeftKeypressImage)
          bottommenu.pack(side=BOTTOM)
      else:
          root.bind('<Left>',ignore)

      if index != (len(filenames)-1):
          bottommenu.pack_forget()
          global next_btn
          next_btn = Button(buttonmenu, text="Next", width=15, command=NextImage)
          next_btn.pack(side=RIGHT)
          root.bind('<Right>', RightKeypressImage)
          bottommenu.pack(side=BOTTOM,fill=Y)
      else:
          root.bind('<Right>',ignore)

      buttonmenu.pack(side=LEFT,fill=Y,padx=50)

      bottommenu.pack_forget()
      global zoommenu
      zoommenu = Frame(bottommenu)

      reset_zoom_btn = Button(zoommenu, text="Reset", command=ResetScale)
      reset_zoom_btn.pack(side=LEFT)
      global zoomscale
      zoomscale = Scale(zoommenu,from_=10, to=200, orient=HORIZONTAL)
      zoomscale.set(scalevalue)
      zoomscale.pack(side=LEFT)
      global zoom_btn
      zoom_btn = Button(zoommenu, text="Zoom", width=10, command=ScaleImage)
      zoom_btn.pack(side=RIGHT)

      zoommenu.pack(anchor=E,padx=20,side=RIGHT)
      bottommenu.pack(side=BOTTOM,fill=BOTH,expand=NO)
    
      string = filenames[index]
      im = Image.open(string)
      imagewidth , imageheight = im.size
      
      im = im.resize((int(imagewidth*factor),int(imageheight*factor)), Image.ANTIALIAS)

      photo = ImageTk.PhotoImage(im)
      canvas.create_image(10,10,anchor=NW, image=photo)

      canvas.configure(width=imagewidth*factor+20,height=imageheight*factor+20)
      canvas.configure(scrollregion=(0,0,imagewidth*factor+20,imageheight*factor+20))
      canvas.place(relx=0.5,rely=0.5,anchor=CENTER)

      hbar=Scrollbar(frame,orient=HORIZONTAL)
      hbar.pack(side=BOTTOM,fill=X)
      hbar.config(command=canvas.xview)
      vbar=Scrollbar(frame,orient=VERTICAL)
      vbar.pack(side=RIGHT,fill=Y)
      vbar.config(command=canvas.yview)
      canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
      frame.pack(expand=YES,fill=BOTH)
      canvas.pack(expand=YES, fill=Y)
      if usedos == 'Windows':
         root.bind("<MouseWheel>", mouse_wheel)
      else:
         root.bind("<Button-4>", mouse_wheel)
         root.bind("<Button-5>", mouse_wheel)
      root.bind('<Up>',ScrollUp)
      root.bind('<Down>',ScrollDown)

def PreviousImage():
      global index
      index = index - 2
      NextImage()

def ScaleImage():
      global index
      global factor
      global zoomscale
      global scalevalue
      
      scalevalue = zoomscale.get()
      factor= zoomscale.get()*0.01      
      index = index -1
      NextImage()

def ResetScale(): 
      global zoomscale
      zoomscale.set(100)     


def RightKeypressImage(event):
      NextImage()

def LeftKeypressImage(event):
      PreviousImage()

def RightKeypressFolder(event):
      NextTen()

def LeftKeypressFolder(event):
      PreviousTen()

def ignore(event):
      pass

def mouse_wheel(event):
     dir = 0
     if usedos == "Windows" :
       if event.delta == -120:
         dir = 2
       if event.delta == 120:
         dir = -2
     else:
       if event.num == 5:
         dir = 2
       if event.num == 4:
         dir = -2
     canvas.yview_scroll(dir, "units")

def ScrollUp(event):
     canvas.yview_scroll(-2, "units")

def ScrollDown(event):
     canvas.yview_scroll(2, "units")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()

root.title("Vertical Viewer")
root.minsize(600, 500)

path = resource_path("viewer.ico")
root.wm_iconbitmap(path)


frame = Frame(root)
frame.pack(expand=YES,fill=BOTH)

init()

mainloop()