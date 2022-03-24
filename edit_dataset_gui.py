import tkinter as tk
import pandas as pd
from PIL import ImageTk, Image  
import sys
import tkinter as tki 
import pickle

def save_exit():
    #save to excel and destroy the window
    global i
    df.to_excel("Image_Age_Gender_Info_Edited.xlsx")
    window.destroy()
    
    #save where you left off
    outfile = open("num_file.pkl", "wb")
    pickle.dump(i, outfile)
    outfile.close()


def next():
    global i

    #update the age
    age_revised = inputtxt.get("1.0","end-1c")
    df.iloc[i,2] = age_revised

    #update the gender
    if gender_wrong.get() == 1:
        if df.iloc[i,3]=="Female":
            df.iloc[i,4]="Male"
        else:
            df.iloc[i,4]="Female"

    #mark not_usable 1 if user marked is_unusable
    if is_unusable.get() == 1:
        df.iloc[i,5] = is_unusable.get()
    

    #update the display
    i = i + 1
    path = "AGE_GENDER_DATA/face_images/" + df.iloc[i,0]
    age = df.iloc[i,1]
    gender = df.iloc[i,3]

    img = Image.open(path)
    img_tk = ImageTk.PhotoImage(img)   
    panel.configure(image = img_tk)
    panel.image = img_tk

    #a label that displays age and gender
    info.configure(text = "age: "+ str(age) + " gender: "+ str(gender))

#read the excel data
dataset_path = "Image_Age_Gender_Info.xlsx"
df = pd.read_excel(dataset_path)

#read the cursor pickle
infile = open("num_file.pkl", "rb")
i =  pickle.load(infile)
infile.close()
#shape is (8253, 6) my part is  [2752, 5503]
#['image_name', 'age', 'age_updated', 'gender', 'gender_updated','not_usable']

#create GUI window and panels    
window = tk.Tk()
panel = tk.Label(window)
panel.pack()

info = tk.Label()
info.pack() 

#get revised age input
inputtxt = tk.Text(window,
                height = 5,
                width = 20)
inputtxt.pack()

#gender_revised checkbox, if checked the gender is wrong. Flip on the dataset
gender_wrong = tk.IntVar()
c0 = tk.Checkbutton(window, text='is gender wrong',
                    variable=gender_wrong, 
                    onvalue=1, 
                    offvalue=0)
c0.pack()

#is_unusable checkbox, if checked the image is unusable. Mark as unusable in the dataset
is_unusable = tk.IntVar()
c1 = tk.Checkbutton(window, text='is unusable?',
                    variable=is_unusable, 
                    onvalue=1, 
                    offvalue=0)
c1.pack()

#next button
button_next = tk.Button(text="next",
                        width=25, height=5,
                        command=next)
button_next.pack()  

#save and exit button
button_save = tk.Button(text="save and exit",
                        width=25, height=5,
                        command=save_exit)
button_save.pack() 

#display the ith image on a tkinter window
path = "AGE_GENDER_DATA/face_images/" + df.iloc[i,0]
age = df.iloc[i,1]
gender = df.iloc[i,3]

img = Image.open(path)
img_tk = ImageTk.PhotoImage(img)   
panel.configure(image = img_tk)

#a label that displays age and gender
info.configure(text = "age: "+ str(age) + " gender: "+ str(gender))
window.mainloop()
