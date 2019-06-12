import cv2
from Tkinter import *
import os
import time
from imutils.video import VideoStream
import threading
import imutils
import cv2
from PIL import Image
from PIL import ImageTk
import numpy as np
from people_count import getcount
cnt = 0
from imutils.video import FPS

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom



def Peoplecount():
	vs=cv2.VideoCapture(0)
	fps = FPS().start()
	#vs = VideoStream(src=0).start()
	vid = Tk()
	app=FullScreenApp(vid)
	global outputPath
	#outputPath = 'Photos/{}/'.format(name1) 
	def videoLoop():
		panel = None
		CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
			"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
			"sofa", "train", "tvmonitor"]
		COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

		# load our serialized model from disk
		print("MODEL LOADING...")
		net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

		try:		
			while True:
				ret,frame = vs.read()
				
				frame,cnt=getcount(frame,CLASSES,net)
				count = Label(vid, text="People :{}".format(cnt))
				count.config(font=labelfont)
				count.place(relx=0.8, rely=0.4, anchor=CENTER)
				frame = imutils.resize(frame, width=700)
				image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if panel is None:
					panel = Label(image=image)
					panel.image = image
					panel.pack(side="left", padx=10, pady=10)
				else:
					panel.configure(image=image)
					panel.image = image
				if cv2.waitKey(1) == 27:
					break
				fps.update()

		except RuntimeError, e:
		 	print("[INFO] caught a RuntimeError")
	
	def onClose():
		print("CLOSING...")
		stopEvent.set()
		vs.release()
		fps.stop()
		cv2.destroyAllWindows()
		#vs.stop()
		vid.destroy()

		
	# if cv2.waitKey(1)==27:
 # 		break
    
	
	exit = Button(vid,text = 'exit',height = 3, width = 20,command=onClose)
	exit.place(relx=0.8, rely=0.6, anchor=CENTER)
	label = Label(vid, text="Number of people in the Room",fg="red")
	label.place(relx=0.8, rely=0.31, anchor=CENTER)
	
	count = Label(vid, text="People :{}".format(cnt))
	labelfont=('times',30,'bold')
	count.config(font=labelfont)

	count.place(relx=0.8, rely=0.4, anchor=CENTER)
	stopEvent = threading.Event()
	thread = threading.Thread(target=videoLoop, args=())
	thread.start()
	vid.wm_title("Camera")
	vid.wm_protocol("WM_DELETE_WINDOW",onClose)
	# start the app
	# pba = PhotoBoothApp(vs)
	mainloop()



if __name__ == "__main__":
		Peoplecount()

