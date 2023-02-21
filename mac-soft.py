from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import filedialog
import platform
import psutil

#brightness
import screen_brightness_control

#audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

#clock
from time import strftime

#calendar 
from tkcalendar import *

#open google
import pyautogui
import subprocess
import webbrowser as wb
import random

IMAG_PATH="C:/Users/ferna/Downloads/python/mac soft/GUI/images/"

root=Tk()
root.title("mac soft Tool")
root.geometry("850x500+300+170")
root.resizable(False, False)
root.configure(bg="#292e2e")

#icon
image_icon=PhotoImage(file=IMAG_PATH+"icons/icon3.png")
root.iconphoto(False, image_icon)

Body=Frame(root, width=900, height=600, bg="#d6d6d6")
Body.pack(padx=20, pady=20)

#left frame
LHS=Frame(Body, width=310, height=435, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1)
LHS.place(x=10, y=10)

#logo laptop
photo_laptop=PhotoImage(file=IMAG_PATH+"Laptop.png")
my_image=Label(LHS, image=photo_laptop, background="#f4f5f5")
my_image.place(x=2, y=10)


my_sistem=platform.uname()

#labels
sistem_name=Label(LHS, text=my_sistem.node, bg="#f4f5f5", font=("Acumin Variable Concept", 15, "bold"), justify="center")
sistem_name.place(x=15, y=200)

sistem_version=Label(LHS, text=f"Version: {my_sistem.version}", bg="#f4f5f5", font=("Acumin Variable Concept", 8), justify="center")
sistem_version.place(x=15, y=225)

sistem_system=Label(LHS, text=f"System: {my_sistem.system}", bg="#f4f5f5", font=("Acumin Variable Concept", 15), justify="center")
sistem_system.place(x=15, y=250)

sistem_machine=Label(LHS, text=f"Machine:{my_sistem.machine}", bg="#f4f5f5", font=("Acumin Variable Concept", 15), justify="center")
sistem_machine.place(x=15, y=285)

sistem_RAM=Label(LHS, text=f"Total RAM installed: {round(psutil.virtual_memory().total/1000000000,2)} GB",
                  bg="#f4f5f5", font=("Acumin Variable Concept", 15), justify="center")
sistem_RAM.place(x=15, y=310)

sistem_processor=Label(LHS, text=f"Processor: {my_sistem.processor}", bg="#f4f5f5", font=("Acumin Variable Concept", 7, "bold"), justify="center")
sistem_processor.place(x=15, y=340)


#right down frame 
RHS=Frame(Body, width=470, height=230, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1)
RHS.place(x=330, y=10)

system=Label(RHS, text="System", font=("Acumin Variable Concept", 15, "bold"), fg="black")
system.place(x=10, y=5)

#CPU FREQ and Disk percent space 
def CPU():
    cpu_freq_current=psutil.cpu_freq().current
    cpu_freq_min=psutil.cpu_freq().min
    cpu_freq_max=psutil.cpu_freq().max

    label_cpu_freq.config(text=f"{cpu_freq_current}%")
    label_freq.config(text=f"CPU min:{cpu_freq_min}%\nCPU max:{cpu_freq_max}%")
    
    CPU_png=PhotoImage(file=IMAG_PATH+"CPU2.png")
    CPU_label=Label(RHS, image=CPU_png, background="#f4f5f5")
    CPU_label.place(x=15, y=40)

def Disk():
    percent_disk_usage=psutil.disk_usage('/').percent
    label_disk.config(text=f"{percent_disk_usage}% disk space usage")

    hard_disk_png=PhotoImage(file=IMAG_PATH+"hardDisk1.png")    
    disk_label=Label(RHS, image=hard_disk_png, background="#f4f5f5")
    disk_label.place(x=15, y=140)


label_cpu_freq=Label(RHS, font=("Acumin Variable Concept", 30, "bold"), fg="black")
label_cpu_freq.place(x=220, y=10)

label_freq=Label(RHS, font=("Acumin Variable Concept", 15), fg="black")
label_freq.place(x=220, y=60)

label_disk=Label(RHS, font=("Acumin Variable Concept", 15), fg="black")
label_disk.place(x=220, y=120)

CPU()
Disk()

#speaker
label_speaker=Label(RHS, text="Speaker", font=('arial', 10, 'bold'), bg="#f4f5f5")
label_speaker.place(x=220, y=160)
volume_value=tk.DoubleVar()

def Get_current_volume_value():
    return "{: .2f}".format(volume_value.get())

def Volume_changed(event):
    device=AudioUtilities.GetSpeakers()
    interface=device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume=cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-float(Get_current_volume_value()), None)

style=ttk.Style()
style.configure("TScale", background="#f4f5f5")

volume=ttk.Scale(RHS, from_=60, to=0, orient="horizontal", command=Volume_changed, variable=volume_value)
volume.place(x=220, y=190)
volume.set(20)

#brightness
label_brightness=Label(RHS, text="Brightness", font=("arial", 10, "bold"), fg="black")
label_brightness.place(x=340, y=160)
current_value=tk.DoubleVar()

def Get_current_value():
    return "{: .2f}".format(current_value.get())

def Brightness_changed(event):
    screen_brightness_control.set_brightness(float(Get_current_value()))

brightness=ttk.Scale(RHS, from_=0, to=100, orient="horizontal", command=Brightness_changed,
                      variable=current_value)
brightness.place(x=340, y=190)

##################################  call to apps  ##################################

#app1 - weather
def weather():
    app1=Toplevel()
    app1.title("Weather App")
    app1.geometry("890x470+300+300")
    app1.configure(bg="#57adff")
    app1.resizable(False, False)

    IMAG_PATH_APPS="C:/Users/ferna/Downloads/python/mac soft/GUI/apps/"

    def getWeather():
        city=textField.get()

        geolocator=Nominatim(user_agent="geoapiExercises")
        location=geolocator.geocode(city)
        obj=TimezoneFinder()

        result=obj.timezone_at(lng=location.longitude, lat=location.latitude)
        timezone.config(text=result)
        lat=location.latitude
        long=location.longitude
        long_lat.config(text=f"lat: {round(lat),4}° N, long: {round(long), 4} ° E")

        home=pytz.timezone(result)
        local_time=datetime.now(home)
        current_time=local_time.strftime("%I:%M %p")
        clock.config(text=current_time)

        API_KEY="2f18cebac7921bdde8279189a7f39841"
        URL="https://api.openweathermap.org/data/2.5/weather"
        parametros={"appid" : API_KEY, "q": city, "units": "metric", "lang":"es"}
        response= requests.get(URL, params=parametros)
        clima=response.json()

        #current
        humidity=clima['main']['humidity']
        pressure=clima['main']['pressure']
        wind=clima['wind']['speed']
        temp_max=clima['main']['temp_max']
        temp_min=clima['main']['temp_min']
        desc=clima["weather"][0]["description"]
        temp=clima["main"]["temp"]

        t.config(text=(temp,"°C"))
        h.config(text=(humidity,"%"))
        p.config(text=(pressure,"hPa"))
        w.config(text=(wind,"m/s"))
        d.config(text=(desc))
        

        #first cell
        firstdayImage=clima['weather'][0]['icon']
        photo1=ImageTk.PhotoImage(file=IMAG_PATH_APPS+f"icon/{firstdayImage}@2x.png")
        firstImage.config(image=photo1)
        firstImage.image=photo1

        day1temp.config(text=f"Max: {temp_max} °C\nMin: {temp_min} °C")


        #days
        first=datetime.now()
        day1.config(text=first.strftime("%A"))
        day1.place(x=210, y=20)


    #icon
    image_icon=PhotoImage(file=IMAG_PATH_APPS+"Images/logo.png")
    app1.iconphoto(False, image_icon)


    Round_box=PhotoImage(file=IMAG_PATH_APPS+"Images/Rounded Rectangle 4.png")
    round_box_label=Label(app1, image=Round_box, bg="#57adff")
    round_box_label.place(x=30, y=110)

    #label
    label1=Label(app1, text="Temperature", font=('Helvetica', 12), fg="white", bg="#203243")
    label1.place(x=50, y=125)

    label2=Label(app1, text="Humidity", font=('Helvetica', 12), fg="white", bg="#203243")
    label2.place(x=50, y=150)

    label3=Label(app1, text="Pressure", font=('Helvetica', 12), fg="white", bg="#203243")
    label3.place(x=50, y=175)

    label4=Label(app1, text="Wind Speed", font=('Helvetica', 12), fg="white", bg="#203243")
    label4.place(x=50, y=200)

    label5=Label(app1, text="Description", font=('Helvetica', 12), fg="white", bg="#203243")
    label5.place(x=50, y=225)


    #search box
    Search_image=PhotoImage(file=IMAG_PATH_APPS+"Images/Rounded Rectangle 3.png")
    myImage=Label(app1, image=Search_image, bg="#57adff")
    myImage.place(x=270, y=120)

    weat_image=PhotoImage(file=IMAG_PATH_APPS+"Images/Layer 7.png")
    weatherImage=Label(app1, image=weat_image, bg="#203243")
    weatherImage.place(x=290, y=127)

    textField=tk.Entry(app1, justify='center', width=15, font=('poppins', 25, 'bold'), bg="#203243", border=0, fg="white")
    textField.place(x=370, y=130)
    textField.focus()

    Search_icon=PhotoImage(file=IMAG_PATH_APPS+"Images/Layer 6.png")
    myImage_icon=Button(app1, image=Search_icon, borderwidth=0, cursor="hand2", bg="#203243", command=getWeather)
    myImage_icon.place(x=645, y=125)

    #Bottom box
    frame=Frame(app1, width=1200, height=180, bg="#212120")
    frame.pack(side=BOTTOM)

    #bottom boxes
    firstbox=PhotoImage(file=IMAG_PATH_APPS+"Images/Rounded Rectangle 2.png")
    Label(frame, image=firstbox, bg="#212120").place(x=150, y=20)


    #clock (place time)
    clock=Label(app1, font=("Helvetic", 30, 'bold'), fg="white", bg="#57adff")
    clock.place(x=30, y=20)


    #timezone
    timezone=Label(app1, font=("Helvetic", 20), fg="white", bg="#57adff")
    timezone.place(x=500, y=20)

    long_lat=Label(app1, font=("Helvetic", 10), fg="white", bg="#57adff")
    long_lat.place(x=500, y=50)

    #thpwd
    t=Label(app1, font=("Helvetica", 12), fg="white", bg="#203243")
    t.place(x=150,y=125)
    h=Label(app1, font=("Helvetica", 12), fg="white", bg="#203243")
    h.place(x=150,y=150)
    p=Label(app1, font=("Helvetica", 12), fg="white", bg="#203243")
    p.place(x=150,y=175)
    w=Label(app1, font=("Helvetica", 12), fg="white", bg="#203243")
    w.place(x=150,y=200)
    d=Label(app1, font=("Helvetica", 12), fg="white", bg="#203243")
    d.place(x=150,y=225)


    #first cell
    firstframe=Frame(app1, width=550,height=132, bg="#282829")
    firstframe.place(x=160,y=315)

    day1=Label(firstframe, font="arial 30", bg="#282829", fg="#fff")
    day1.place(x=120, y=5)

    firstImage=Label(firstframe, bg="#282829")
    firstImage.place(x=80, y=15)

    day1temp=Label(firstframe, bg="#282829", fg="#57adff", font="arial 15 bold")
    day1temp.place(x=210, y=72)


    app1.mainloop()

################################## app2 clock ###########################

#clock app
def Clock_app():
    IMAG_PATH_APPS="C:/Users/ferna/Downloads/python/mac soft/GUI/apps/"
    app2=Toplevel()
    app2.geometry("850x110+300+10")
    app2.title("Clock")
    app2.configure(bg="#292e2e")
    app2.resizable(False, False)

    #icon
    image_icon_clock=PhotoImage(file=IMAG_PATH_APPS+"Images/Rounded Rectangle 2.png")
    app2.iconphoto(False, image_icon_clock)

    def clock():
        text=strftime("%H:%M:%S %p")
        label_clock.config(text=text)
        label_clock.after(1000, clock)

    label_clock=Label(app2, font=("digital-7", 50, "bold"), width=20, bg="#f4f5f5", fg="#292e2e")
    label_clock.pack(anchor="center", pady=20)
    clock()
    app2.mainloop()



################################## app3 calendar ###########################
#calendar app

def Calendar_app():
    IMAG_PATH_APPS="C:/Users/ferna/Downloads/python/mac soft/GUI/apps/"

    app3=Toplevel()
    app3.geometry("300x300+-10+10")
    app3.title("Calendar")
    app3.configure(bg="#292e2e")
    app3.resizable(False, False)

    #icon
    image_icon_calendar=PhotoImage(file=IMAG_PATH_APPS+"Images/calendar.png")
    app3.iconphoto(False, image_icon_calendar)

    my_calendar=Calendar(app3, setmode="day", date_pattern="d/m/yy")
    my_calendar.pack(padx=15, pady=35)

    app3.mainloop()

###################################     app4 dark mode    ####################################
button_mode=True

def mode():
    global button_mode
    if button_mode:
        LHS.config(bg="#292e2e")
        my_image.config(bg="#292e2e")
        label_brightness.config(bg="#292e2e", fg="#d6d6d6")
        label_cpu_freq.config(bg="#292e2e", fg="#d6d6d6")
        label_disk.config(bg="#292e2e", fg="#d6d6d6")
        label_freq.config(bg="#292e2e", fg="#d6d6d6")
        label_speaker.config(bg="#292e2e", fg="#d6d6d6")
        
        
        RHB.config(bg="#292e2e")
        apps.config(bg="#292e2e", fg="#d6d6d6")
        app1.config(bg="#292e2e")
        app2.config(bg="#292e2e")
        app3.config(bg="#292e2e")
        app4.config(bg="#292e2e")
        app5.config(bg="#292e2e")
        app6.config(bg="#292e2e")
        app7.config(bg="#292e2e")
        app8.config(bg="#292e2e")
        app9.config(bg="#292e2e")
        app10.config(bg="#292e2e")    
        
        RHS.config(bg="#292e2e")

        button_mode=False

    else:
        LHS.config(bg="#f4f5f5")
        my_image.config(bg="#f4f5f5")
        label_brightness.config(bg="#f4f5f5", fg="#292e2e")
        label_cpu_freq.config(bg="#f4f5f5", fg="#292e2e")
        label_disk.config(bg="#f4f5f5", fg="#292e2e")
        label_freq.config(bg="#f4f5f5", fg="#292e2e")
        label_speaker.config(bg="#f4f5f5", fg="#292e2e")
        
        
        RHB.config(bg="#f4f5f5")
        apps.config(bg="#f4f5f5", fg="#292e2e")
        app1.config(bg="#f4f5f5")
        app2.config(bg="#f4f5f5")
        app3.config(bg="#f4f5f5")
        app4.config(bg="#f4f5f5")
        app5.config(bg="#f4f5f5")
        app6.config(bg="#f4f5f5")
        app7.config(bg="#f4f5f5")
        app8.config(bg="#f4f5f5")
        app9.config(bg="#f4f5f5")
        app10.config(bg="#f4f5f5")    
        
        RHS.config(bg="#f4f5f5")

        button_mode=True

######################################## app5 Random dices ##################################################

def game():
    IMAG_PATH_APPS="C:/Users/ferna/Downloads/python/mac soft/GUI/apps/"

    app5=Toplevel()
    app5.geometry("700x600+1170+170")
    app5.title("Random Dices")
    app5.configure(bg="#dee2e5")
    app5.resizable(False, False)

    #icon
    image_icon_dices=PhotoImage(file=IMAG_PATH_APPS+"Images/dices.png")
    app5.iconphoto(False, image_icon_dices)

    dice_image=PhotoImage(file=IMAG_PATH_APPS+"Images/ludo.png")
    Label(app5, image=dice_image).pack()

    label_dice=Label(app5, text='', font=("times", 150))
    
    def roll():
        dice=['\u2680', '\u2681','\u2682','\u2683','\u2684', '\u2685']
        label_dice.configure(text=f"{random.choice(dice)}{random.choice(dice)}", fg="#29232e")
        label_dice.pack()
    
    btn_image=PhotoImage(file=IMAG_PATH_APPS+"Images/roll.png")
    btn=Button(app5, image=btn_image, bg="#dee2e5", command=roll)
    btn.pack(padx=10, pady=10)

    app5.mainloop()

######################## app6 screenshot ####################

def screenshot():
    root.iconify()
    myScreenshot=pyautogui.screenshot()
    file_path=filedialog.asksaveasfilename(defaultextension='.png', filetypes=(("File Png", "*.png"), 
                                                             ("File jpg", "*.jpg"),   
                                                             ("File jpge", "*.jpge"),
                                                             ("All files", "*.*")))
    myScreenshot.save(file_path)
    

######################## app7  ####################

def desktop():
    subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')

def crome():
    wb.register('chrome', None)
    wb.open('https://www.google.com/')

def youtube():
    wb.register('chrome', None)
    wb.open('https://www.youtube.com/')

def close_apps():
    root.destroy()

#Apps
RHB=Frame(Body, width=470, height=190, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1)
RHB.place(x=330, y=255)

apps=Label(RHB, text="Apps", font=("Acumin Variable Concept", 15), fg="black")
apps.place(x=10, y=10)

app1_image=PhotoImage(file=IMAG_PATH+"weather_icon3.png")
app1=Button(RHB, image=app1_image, command=weather)
app1.place(x=10, y=40)

app2_image=PhotoImage(file=IMAG_PATH+"clock2.png")
app2=Button(RHB, image=app2_image, command=Clock_app)
app2.place(x=100, y=40)

app3_image=PhotoImage(file=IMAG_PATH+"calendar.png")
app3=Button(RHB, image=app3_image, command=Calendar_app)
app3.place(x=185, y=40)

app4_image=PhotoImage(file=IMAG_PATH+"brightness.png")
app4=Button(RHB, image=app4_image, command=mode)
app4.place(x=270, y=40)

app5_image=PhotoImage(file=IMAG_PATH+"dices.png")
app5=Button(RHB, image=app5_image, command=game)
app5.place(x=355, y=40)

app6_image=PhotoImage(file=IMAG_PATH+"screenshoot3.png")
app6=Button(RHB, image=app6_image, command=screenshot)
app6.place(x=10, y=110)

app7_image=PhotoImage(file=IMAG_PATH+"desktop2.png")
app7=Button(RHB, image=app7_image, command=desktop)
app7.place(x=100, y=110)

app8_image=PhotoImage(file=IMAG_PATH+"google4.png")
app8=Button(RHB, image=app8_image, command=crome)
app8.place(x=185, y=110)

app9_image=PhotoImage(file=IMAG_PATH+"youtube.png")
app9=Button(RHB, image=app9_image, command=youtube)
app9.place(x=270, y=110)

app10_image=PhotoImage(file=IMAG_PATH+"close3.png")
app10=Button(RHB, image=app10_image, command=close_apps)
app10.place(x=355, y=110)

root.mainloop()