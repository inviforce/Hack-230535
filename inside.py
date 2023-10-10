from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as ttb
from PIL import Image, ImageTk
import customtkinter
import storage
import subprocess
from dotenv import load_dotenv
import requests
import os
import storage
import threading
load_dotenv()
customtkinter.set_appearance_mode("dark")
root1=ttb.Window(themename="cyborg")
root1.title("TEMPERATURE_ALERT(Hack-230535)")
root1.geometry('1400x1400')
image1 = Image.open("Logo_techfest.png")
resize_image = image1.resize((300, 220))
img = ImageTk.PhotoImage(resize_image)
label1 = Label(image=img)
label1.image1 = img
label1.place(x=0, y=0)
my_label=ttb.Label(text="Temperature \n       Alert",font=("arial black",30),bootstyle="light",relief="flat")
my_label.place(anchor = CENTER, relx = .5, rely = 0.07)
def update_information():
    weather_api_key=os.getenv('weather_api_key')
    weather_api=f'https://api.openweathermap.org/data/2.5/weather?q={storage.Location}&appid={weather_api_key}'
    params={"units":"metric"}
    response_api=requests.get(weather_api,params=params)
    content = response_api.json()
    text_new=f"Location:{storage.Location}\nminimum temperature: {storage.min_temp}°C\nmaximum temperature: {storage.max_temp}°C"
    my_label.config(text=text_new)
    text2_new=f'Hi {storage.username}\ncurrent temperature is {content["main"]["temp"]}°C'
    welcome_label.config(text=text2_new)
    text3_new=f'Advanced information\nHumidity:{content["main"]["humidity"]}%\nVisibility:{content["visibility"]}meter\nPressure:{content["main"]["pressure"]}hPa\nWind Speed:{content["wind"]["speed"]}m/s'
    info_label.config(text=text3_new)
class CountdownTimerApp:
    def __init__(self, root):
        self.root = root
        
        self.time_remaining = 30* 60  # 30 minutes in seconds
        self.running = True

        self.label = ttb.Label(root, text="", font=("Helvetica", 48))
        self.label.place(anchor = NE,relx = 1, rely = 0)

        self.update_timer()

    def update_timer(self):
        if self.running:
            if self.time_remaining > 0:
                minutes, seconds = divmod(self.time_remaining, 60)
                time_string = f"{minutes:02d}:{seconds:02d}"
                self.label.config(text=time_string)
                self.time_remaining -= 1
            else:
                self.time_remaining = 30 * 60  # to restart the timer
                update_information()
        self.root.after(1000, self.update_timer)  
my_frame = customtkinter.CTkFrame(master=root1,width=450,height=80,border_color="white",border_width=2
,fg_color="transparent",corner_radius=15)
my_frame.place(anchor = CENTER, relx = .5, rely = 0.23)
my_label=Label(my_frame,text="",
font=("cooper",15),justify="left")
my_label.place(x=15,y=3)
welcome_label=Label(root1,text="",
font=("arial black",18),justify="left")
welcome_label.place(x=20,y=310)
my_chatbox=customtkinter.CTkScrollableFrame(master=root1,width=400,height=340,border_color="red",border_width=4
,fg_color="transparent",corner_radius=15)
my_chatbox.place(x=10,y=300)
chatbox_label=Label(my_chatbox,text="NOTIFICATION BOX",font=("cooper",20))
chatbox_label.pack()
def run_command():
    # to run python terminal in gui frame
    global process
    process = subprocess.Popen(["python", "temperature.py"],stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
    universal_newlines=True)
    for line in process.stdout:
        label_temp=Label(my_chatbox,text=line,font=("cooper",15),wraplength=600)
        label_temp.pack()
def why_on_earth():
    CountdownTimerApp(root1)
    thread1 = threading.Thread(target=run_command)
    thread1.start()
info_frame=customtkinter.CTkFrame(master=root1,width=350,height=160,border_color="white",border_width=4
,fg_color="transparent",corner_radius=15)
info_frame.place(anchor = E,relx = 0.9, rely = 0.6)
info_label=Label(master=root1,
text="",
font=("cooper",18),justify="left")
info_label.place(anchor = E,relx = 0.83, rely = 0.6)
def exit():
    process.terminate()
    root1.destroy()
my_style=ttb.Style()
my_style.configure("danger.TButton",font=("Helvetica",15),width=20,height=20)
my_button=ttb.Button(root1,text="EXIT",bootstyle="danger",command=exit, style="danger.TButton")
my_button.place(x=850,y=950)
my_button1=ttb.Button(root1,text="START ALERT",bootstyle="danger",command=why_on_earth, style="danger.TButton")
my_button1.place(x=850,y=850)
update_information()
root1.mainloop()
