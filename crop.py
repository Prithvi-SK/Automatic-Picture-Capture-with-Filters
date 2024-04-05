from tkinter import *
import numpy as np 
from PIL import Image,ImageTk
import cv2
from new import *


root=Tk()
image=cv2.imread("Lenna.png")
img = ImageTk.PhotoImage(Image.open("Lenna.png"))

def select():
   
   c_image=image[int(scale1.get()):int(scale2.get()),int(scale3.get()):int(scale4.get())]
   #cv2.imshow("cropped",c_image)
   cv2.imwrite("cropped.png",c_image)



label=Label(image=img)
label.image=img
label.grid(row=0,column=0)

hi = IntVar()  
scale1 = Scale(root, variable = hi,length=512 ,from_ = 0, to = 512, orient = HORIZONTAL)

scale1.grid(row=1,column=0)
hf=IntVar()
scale2 = Scale(root, variable = hf,length=512 ,from_ = 0, to = 512, orient = HORIZONTAL)
scale2.grid(row=2,column=0)
hiv=IntVar()
scale3 = Scale(root, variable = hiv,length=512 ,from_ = 0, to = 512, orient = VERTICAL)
scale3.grid(row=0,column=1)

hfv=IntVar()
scale4 = Scale(root, variable = hfv,length=512 ,from_ = 0, to = 512, orient =VERTICAL)
scale4.grid(row=0,column=2)

btn = Button(root, text="Update", command=select)  
btn.grid(row=3,column=3)



#jolt()

root.mainloop()


