# !/usr/bin/python3
 
import tkinter as tk
import requests
import json
import datetime
import re
import gtts
import webbrowser
from tkinter import ttk
from tkinter import messagebox
from playsound import playsound 
from fake_useragent import UserAgent
  
root=tk.Tk()
root.title("Vaccine Slot Notifier (with voice alerts)")

# Setting icon of master window
icon = tk.PhotoImage(file=r"D:\PersonalProjects_andFiles\python_projects\slot_checker_v2\app_icon.png") 
root.iconphoto(False, icon)
 
# setting the window size
root.geometry("400x400")
root.minsize(width=400, height=400)
root.maxsize(width=400, height=400)
root.configure(bg='light blue')


#default values
pin_code = "00"
user_age_limit = 18
user_selected_dose = "available_capacity_dose1"

#defining the text for the audio files  
t1 = gtts.gTTS("slots checking started, you will be notified with voice alert when a slot is available")  
t2 = gtts.gTTS("slots available")

# save the audio file  
t1.save("welcome.mp3")
t2.save("slot_avail.mp3") 


open_slot_found_flag = 0

#creating temperory user for the api
temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}

name_var=tk.StringVar()


def change_date_format():
        date = str(datetime.date.today()) 
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', date)


def get_user_age():
    entered_age = age_selector.get()
    if(entered_age == "45+"):
        return (int(45))
    else:
        return (int(18))
 

def get_user_required_dose():
    entered_dose = dose_selector.get()
    if (entered_dose == "Dose 1"):
        return (str('available_capacity_dose1'))
    else:
        return (str('available_capacity_dose2'))


def slot_availability_loop():
    if (open_slot_found_flag):
        print("final step")
        playsound("slot_avail.mp3")
        root.after(2000, slot_availability_loop)
        
        

def main():
    global open_slot_found_flag
    global user_age_limit
    global user_selected_dose

    
    user_pin_code = pin_entry.get()
    user_age_limit = get_user_age()
    user_selected_dose = get_user_required_dose()

    
    if ((len(user_pin_code) == 6) & (user_pin_code.isdecimal())):
        
        current_date = change_date_format() 
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=&date="
        URL = URL[:83] + user_pin_code + URL[83:]
        URL = URL[:95] + current_date + URL[95:]
        
        try:
            # sending get request and saving the response as response object
            response = requests.get(url = URL, headers = browser_header)
            parsed = json.loads(response.text)
            #print(json.dumps(parsed, indent=4, sort_keys=True))

            #check for available no. of hospitals
            available_hospitals_nos = len(parsed['centers'])

            for i in range(available_hospitals_nos):                                          ##center loop
                center_index = i
                visible_sessions_nos = len(parsed['centers'] [center_index] ['sessions'])
                for j in range(visible_sessions_nos):                                          ##sessions loop
                    session_index = j
                    if ((parsed['centers'] [center_index] ['sessions'] [session_index] ['min_age_limit']) ==  user_age_limit):
                        if ((parsed['centers'] [center_index] ['sessions'] [session_index] [user_selected_dose]) > 0):         ##if slot available
                            print ("slots availale")
                            var.set("slots availale")
                            open_slot_found_flag = 1
                            break
                        else:
                            print ("slot full")
                    else:
                        print ("slots for age 18+ not available")

                        
            if (open_slot_found_flag):
                root.after(2000, slot_availability_loop)

            else:    
               root.after(5000, main)

        except:
            if (open_slot_found_flag == 0):
                var.set("oops! something went wrong")
                print("oops! something went wrong")
                root.after(5000, main)

                
    else:
        var.set("invalid pincode")
        print ("invalid pincode")    
    

      

def start_button_cb():
    
    # play the audio file 
    playsound("welcome.mp3")
    var.set("Slots checking in  progress")
    main()



def callback(url):
    webbrowser.open_new(url)    
     

def cb():
        messagebox.showinfo("How To Use", "Type a valid pincode and select the desired dose number and the age range from the two drop down menu and click start checking button. Turn the volume of the speakers up in order to hear the voice alerts. .\n\nPLEASE"
                            "CHANGE THE SLEEP SETTINGS OF YOUR PC TO AVOID THE PC GOING INTO SLEEP MODE IN ORDER TO KEEP THE SOFTWARE RUNNING IN THE BACKGROUND.")

  

# creating a label for
pin_label = tk.Label(root, text = 'Pincode', highlightthickness = 0, font=('calibre',10,'bold'))
pin_label.place(x=80, y=80)

# creating a entry for input
pin_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))
pin_entry.place(x=150, y=80)

# creating age selector label
age_label = tk.Label(root, text = 'Age', font = ('calibre',10,'bold'))
age_label.place(x=90, y=110)
age_selector = ttk.Combobox(root, width = 20, textvariable = 12)
# Adding combobox drop down list
age_selector['value'] = ('18+', '45+')  
age_selector.place(x=150, y=110)  
age_selector.current(0)

#creating a label for dose number label
dose_label = tk.Label(root, text = 'Dose no.', font = ('calibre',10,'bold'))
dose_label.grid(row=0,column=0)
dose_label.place(x=77, y=140)

#creating a entry for dose number
dose_selector = ttk.Combobox(root, width = 20, textvariable = 6)
# Adding combobox drop down list
dose_selector['value'] = ('Dose 1', 'Dose 2')  
dose_selector.grid(column = 0, row = 0)
dose_selector.place(x=150, y=140)
dose_selector.current(0)

# creating a start button
sub_btn=tk.Button(root,text = 'Start Checking', command = start_button_cb)
sub_btn.grid(row=0,column=0)
sub_btn.place(x=160, y=190)

#creating a label to display the status of the application 
var = tk.StringVar()
label = tk.Message( root, textvariable = var, width = 500 )
var.set("Hey! How are you doing?")
label.place(relx = 0.5, y = 250,anchor = 'center')

#creating icon image for linkedin
photo = tk.PhotoImage(file = r"D:\PersonalProjects_andFiles\python_projects\slot_checker_v2\linkedin_logo.png")
photoimage = photo.subsample(7, 7)
link1 = tk.Label(root, image=photoimage, cursor="hand2")
link1.pack()
link1.place(x=350, y=350)
link1.bind("<Button-1>", lambda e: callback("http://www.linkedin.com/in/sanket-hiremath"))

#creating icon image for github
photo2 = tk.PhotoImage(file = r"D:\PersonalProjects_andFiles\python_projects\slot_checker_v2\github_logo.png")
photoimage2 = photo2.subsample(7, 7)
link2 = tk.Label(root, image=photoimage2, fg="blue", cursor="hand2")
link2.pack()
link2.place(x=310, y=350)
link2.bind("<Button-1>", lambda e: callback("http://www.github.com/SanketHiremath/Vaccination-Slot-Notifier"))

#creating icon image for instructions
photo3 = tk.PhotoImage(file = r"D:\PersonalProjects_andFiles\python_projects\slot_checker_v2\how_to_icon.png")
photoimage3 = photo3.subsample(7, 7)
link3 = tk.Button(root, image = photoimage3, command = cb)
link3.pack()
link3.place(x=360, y=0)



#developer name label
pin_label = tk.Label(root, text = 'Developed by Sanket Hiremath',fg = "green", highlightthickness = 0, font=('calibre',10))
pin_label.place(x=2, y=365)

# performing an infinite loop
root.mainloop()
