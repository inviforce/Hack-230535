from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as ttb
import customtkinter
from tkinter import *
import subprocess
customtkinter.set_appearance_mode("dark")
root=ttb.Window(themename="cyborg")
root.title("TEMPERATURE_ALERT(Hack-230535)")
root.geometry('1400x1400')
my_label=ttb.Label(text="Temperature\n       Alert",font=("arial black",30),bootstyle="light",relief="flat")
my_label.pack()
my_frame = customtkinter.CTkFrame(master=root,width=500,border_color="white",border_width=2
,fg_color="transparent",corner_radius=15) 
my_frame.pack(padx=20,pady=20)
my_label1=ttb.Label(my_frame,text="USER INFORMATION",font=("cooper",25))
my_label1.pack(pady=20)
my_username=customtkinter.CTkEntry(my_frame,placeholder_text="Username",
height=50,width=400,font=("copper",18),corner_radius=50,
text_color="white")
my_username.pack(pady=10)
my_city=customtkinter.CTkEntry(my_frame,placeholder_text="Location",
height=50,width=400,font=("copper",18),corner_radius=50,
text_color="white")
my_city.pack(pady=10,padx=40)
my_mintemp=customtkinter.CTkEntry(my_frame,placeholder_text="Minimum Temperature",
height=50,width=400,font=("copper",18),corner_radius=50,
text_color="white")
my_mintemp.pack(pady=10)
my_maxtemp=customtkinter.CTkEntry(my_frame,placeholder_text="Maximum Temperature",
height=50,width=400,font=("copper",18),corner_radius=50,
text_color="white")
my_maxtemp.pack(pady=10)
def login():
    add()
    root.destroy()
    subprocess.run(["python","inside.py"],check=True)
    
my_style=ttb.Style()
my_style.configure("danger.TButton",font=("Helvetica",15))
my_button=ttb.Button(my_frame,text="RUN",bootstyle="danger",command=login, style="danger.TButton")
my_button.pack(pady=50)
def checker():
    return
var1=IntVar()
def add():
    a=str(my_username.get())
    b=str(my_city.get())
    c=int(my_maxtemp.get())
    d=int(my_mintemp.get())
    with open("storage.py","w") as storage:
        storage.write(f'username="{a}"\nLocation="{b}"\nmax_temp={c}\nmin_temp={d}\n')
    storage.close()
    
    

root.mainloop()