import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from garmin_class import GarminApp
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 
garmin = GarminApp()

def load_screen() -> None: #Function for coding adjustment. Makes user enter new data everytime function is run or allows them to load existing right away.
    popup6 = tk.Toplevel(root)
    popup6.title("Load Existing Data or Create New Profile")

    tk.Label(popup6, text = "Create New Profile", font = ("Impact", 60)).grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20)
    tk.Label(popup6, text = "Load Existing File", font = ("Impact", 60)).grid(row = 0, column = 2, padx = 20, pady = 20)
    tk.Label(popup6, text = "Click Button Below", font = (FONT, 18)).grid(row = 1, column = 2, padx = 5, pady = 5)
    tk.Label(popup6, text = "Enter data for all fields below", font = (FONT, 25)).grid(row = 1, column = 0, columnspan = 2, padx = 20, pady = 20)
    tk.Label(popup6, text = "Full Name (First Last):", font = (FONT, 18)).grid(row = 2, column = 0, padx = 5, pady = 5)
    name_entry = tk.Entry(popup6, font = (FONT, 18))
    name_entry.grid(row = 2, column = 1, padx = 5, pady = 5)
    tk.Label(popup6, text = "Age (years): ", font = (FONT, 18)).grid(row = 3, column = 0, padx = 5, pady = 5)
    age_entry = tk.Entry(popup6, font = (FONT, 18))
    age_entry.grid(row = 3, column = 1, padx = 5, pady = 5)
    tk.Label(popup6, text = "Height (cm): ", font = (FONT, 18)).grid(row = 4, column = 0, padx = 5, pady = 5)
    height_entry = tk.Entry(popup6, font = (FONT, 18))
    height_entry.grid(row = 4, column = 1, padx = 5, pady = 5)
    tk.Label(popup6, text = "Weight (kg): ", font = (FONT, 18)).grid(row = 5, column = 0, padx = 5, pady = 5)
    weight_entry = tk.Entry(popup6, font = (FONT, 18))
    weight_entry.grid(row = 5, column = 1, padx = 5, pady = 5)
    tk.Label(popup6, text = "Gender (Male/Female): ", font = (FONT, 18)).grid(row = 6, column = 0, padx = 5, pady = 5)
    gender_entry = tk.Entry(popup6, font = (FONT, 18))
    gender_entry.grid(row = 6, column = 1, padx = 5, pady = 5)

    def submit_load_screen() -> None: #Reconfigure labels and update class with data
        garmin.submit_data(name_entry.get(), int(age_entry.get()), float(height_entry.get()), float(weight_entry.get()), gender_entry.get())
        name_label.config(text = f"Name: {garmin.name}")
        age_label.config(text = f"Age: {garmin.age}")
        height_label.config(text = f"Height: {garmin.height:.2f}")
        weight_label.config(text = f"Weight: {garmin.weight:.1f} kg")
        bmi_label.config(text = f"BMI: {garmin.bmi:.2f}")
        popup6.destroy()
    
    def load_existing() -> None: #Loading existing file
        load_file()

    submit_button = tk.Button(popup6, text = "Create Profile", font = (FONT, 18), command = submit_load_screen)
    submit_button.grid(row = 7, column = 1, padx = 5, pady = 5)

    load_existing_button = tk.Button(popup6, text = "Load Existing File", font = (FONT, 18), command = load_existing)
    load_existing_button.grid(row = 2, column = 2, padx = 5, pady = 5)

    
def display_all_time() -> None: #Displaying all time stats of running, biking, and swimming
    popup4 = tk.Toplevel(root)
    popup4.title("All Time Stats")

    run_frame = tk.Frame(popup4)
    run_frame.grid(row = 0, column = 0)
    swim_frame = tk.Frame(popup4)
    swim_frame.grid(row = 0, column = 1)
    bike_frame = tk.Frame(popup4)
    bike_frame.grid(row = 0, column = 2)

    total_run_distance = 0
    total_bike_distance = 0
    total_swim_distance = 0
    total_run_time = 0
    total_bike_time = 0
    total_swim_time = 0

    #Tally up totals
    for activity in garmin.activities:
        match activity['type']:
            case "Run":
                total_run_distance += activity['distance']
                total_run_time += activity['time']
            case "Swim":
                total_swim_distance += activity['distance']
                total_swim_time += activity['time']
            case "Bike":
                total_bike_distance += activity['distance']
                total_bike_time += activity['time']

    #Lines to print as labels
    run_lines = [
        f"Running Stats",
        f"Total Runs: {garmin.total_runs}",
        f"Total Distance: {total_run_distance:.2f} km",
        f"Total Time: {total_run_time:.2f} min",
        f"Avg Run Distance: {(total_run_distance / garmin.total_runs if garmin.total_runs != 0 else 0):.2f} km",
        f"Avg Run Time: {(total_run_time / garmin.total_runs if garmin.total_runs != 0 else 0):.2f} min",
        f"Avg Run Pace: {(total_run_time / total_run_distance if total_run_distance != 0 else 0):.2f} min/km",
        f"Avg Run Speed: {(total_run_distance / (total_run_time / 60) if total_run_time != 0 else 0):.2f} km/h"
    ]

    bike_lines = [
        f"Biking Stats",
        f"Total Bike: {garmin.total_bikes}",
        f"Total Distance: {total_bike_distance:.2f} km",
        f"Total Time: {total_bike_time:.2f} min",
        f"Avg Bike Distance: {(total_bike_distance / garmin.total_bikes if garmin.total_bikes != 0 else 0):.2f} km",
        f"Avg Bike Time: {(total_bike_time / garmin.total_bikes if garmin.total_bikes != 0 else 0):.2f} min",
        f"Avg Bike Pace: {(total_bike_time / total_bike_distance if total_bike_distance != 0 else 0):.2f} min/km",
        f"Avg Bike Speed: {(total_bike_distance / (total_bike_time / 60) if total_bike_time != 0 else 0):.2f} km/h"
    ]

    swim_lines = [
        f"Swimming Stats",
        f"Total Swims: {garmin.total_swims}",
        f"Total Distance: {total_swim_distance:.2f} km",
        f"Total Time: {total_swim_time:.2f} min",
        f"Avg Swim Distance: {(total_swim_distance / garmin.total_swims if garmin.total_swims != 0 else 0):.2f} km",
        f"Avg Swim Time: {(total_swim_time / garmin.total_swims if garmin.total_swims != 0 else 0):.2f} min",
        f"Avg Swim Pace: {(total_swim_time / total_swim_distance if total_swim_distance != 0 else 0):.2f} min/km",
        f"Avg Swim Speed: {(total_swim_distance / (total_swim_time / 60) if total_swim_time != 0 else 0):.2f} km/h"
    ]

    #Print all labels
    for line in run_lines:
        if line == "Running Stats":
            label = tk.Label(run_frame, text = line, font = (FONT, 22), anchor = "w", width = 23)
            label.pack(padx = 20, pady = 10, anchor = "w") 
        else:
            label = tk.Label(run_frame, text = line, font = (FONT, 18), anchor = "w", width = 23)
            label.pack(padx = 20, pady = 10, anchor = "w") 
    for line in bike_lines:
        if line == "Biking Stats":
            label = tk.Label(bike_frame, text = line, font = (FONT, 22), anchor = "w", width = 23)
            label.pack(padx = 20, pady = 10, anchor = "w") 
        else:
            label = tk.Label(bike_frame, text = line, font = (FONT, 18), anchor = "w", width = 23)
            label.pack(padx = 20, pady = 10, anchor = "w") 
    for line in swim_lines:
        if line == "Swimming Stats":
            label = tk.Label(swim_frame, text = line, font = (FONT, 22), anchor = "w", width = 23)
            label.pack(padx = 20, pady = 10, anchor = "w") 
        else:
            label = tk.Label(swim_frame, text = line, font = (FONT, 18), anchor = "w", width = 23)
            label.pack(padx = 20, pady = 10, anchor = "w") 

def graphing() -> None:
    for widget in graph_frame.winfo_children():
        widget.destroy() #Remove existing graph to replace with new one
    today = datetime.now().date()
    last_7_days = [today - timedelta(days = i) for i in range(6, -1, -1)]  #List of last 7 days
    day_labels = [d.strftime("%m/%d") for d in last_7_days]
    activity_counts = [0, 0, 0, 0, 0, 0, 0] #Counter for number of activities

    for activity in garmin.activities:
        activity_date = datetime.strptime(activity["date"], "%Y-%m-%d").date()
        if activity_date in last_7_days:
            index = last_7_days.index(activity_date)
            activity_counts[index] += 1 #Tally up number of activites for all 7 days
    
    fig, ax = plt.subplots(figsize = (3.2, 2), dpi = 100) #Sizing for graph and axes
    fig.subplots_adjust(left = 0.12, right = 0.95, top = 0.85, bottom = 0.2) #Padding
    ax.plot(day_labels, activity_counts, marker = 'o', linewidth = 2) 
    ax.set_title("Total Activities in Last 7 Days", fontname = FONT, fontsize = 10)
    ax.set_ylabel("Number of Activities", fontname = FONT, fontsize = 8) #Title and axis label
    ax.set_ylim(0, max(3, max(activity_counts) + 1)) #Scaling for y-axis
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer = True)) #Only integers for y-axis
    ax.grid(True)

    ax.tick_params(axis = 'both', labelsize = 7)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontname(FONT) #x-axis labels

    canvas = FigureCanvasTkAgg(fig, master = graph_frame) #Place in graph_frame
    canvas.draw()
    canvas.get_tk_widget().pack(expand = True, anchor = "center")

def update_datetime() -> None: #Update the time every 1000ms/1s
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    date_string = now.strftime("%A, %B %d %Y")  
    time_string = now.strftime("%H:%M:%S")

    date_label.config(text = date_string + "   " + time_string + " EST")
    root.after(1000, update_datetime) 

def show_activity_details(event) -> None: #Gives detail when an activity in the activity listbox is clicked
    try:
        index = activity_listbox.curselection()[0]
        activity = garmin.activities[index] #Adjust indexing as activities are added to top of listbox but end of dictionary

        date = activity["date"]
        activity_type = activity["type"]
        distance = activity["distance"]
        time = activity["time"]
        pace = time / distance 
        speed = distance / (time / 60)  
        calories = garmin.calculate_calories_burned(distance, activity_type)

        popup3 = tk.Toplevel(root)
        popup3.title("Activity Details")
        popup3.geometry("500x500")

        #Statistics for each run
        info_lines = [
            f"Date: {date}",
            f"Type: {activity_type}",
            f"Distance: {distance:.2f} km",
            f"Time: {time:.2f} min",
            f"Avg Pace: {pace:.2f} min/km",
            f"Avg Speed: {speed:.2f} km/h",
            f"Calories Burned: {calories} Calories Burned"
        ]

        for line in info_lines:
            label = tk.Label(popup3, text = line, font = (FONT, 18), anchor = "w")
            label.pack(padx = 20, pady = 10, anchor = "w") #Label creation for all 7 data fields

        tk.Button(popup3, text = "Close Tab", font = (FONT, 18), command = popup3.destroy).pack(padx = 10, pady = 10)

        def delete_activity() -> None: #Delete an entry
            match activity_type:
                #Subtract 1 from totals
                case "Run":
                    garmin.total_runs = max(0, garmin.total_runs - 1)
                case "Swim":
                    garmin.total_swims = max(0, garmin.total_swims - 1)
                case "Bike":
                    garmin.total_bikes = max(0, garmin.total_bikes - 1)
            garmin.activities.pop(index)
            activity_listbox.delete(0, tk.END)
            for activity in garmin.activities:
                entry = f"{activity['date']} - {activity['type']} - {activity['distance']:.2f} km - {activity['time']:.2f} min"
                activity_listbox.insert(tk.END, entry)
            graphing()
            update_weekly_goal_progress()
            popup3.destroy()
        delete_activity_button = tk.Button(popup3, text = "Delete Activity", font = (FONT, 18), command = delete_activity)
        delete_activity_button.pack(padx = 10, pady = 10)

    except:
        pass

def add_activity() -> None: #Adding activity using distance, time, and activity type
    popup = tk.Toplevel(root)
    popup.title(f"Add {activity_type.get()} Activity")
    popup.geometry("700x250")

    #Get Distance
    distance_label = tk.Label(popup, text = "Distance (Kilometers): ", font = (FONT, 24))
    distance_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")

    distance_entry = tk.Entry(popup, font = (FONT, 24))
    distance_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
    #Get Time
    time_label = tk.Label(popup, text = "Time (Minutes): ", font = (FONT, 24))
    time_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")

    time_entry = tk.Entry(popup, font = (FONT, 24))
    time_entry.grid(row = 1, column = 1, padx = 10, pady = 10)

    def submit() -> None: #Submitting function 
        try:
            distance = float(distance_entry.get())
            time = float(time_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter integer or decimal values only!")
            return
        now = datetime.now().strftime("%Y-%m-%d")
        garmin.update_activity(now, activity_type.get(), distance, time)
        activity_listbox.delete(0, tk.END)
        for activity in garmin.activities:
            entry = f"{activity['date']} - {activity['type']} - {activity['distance']:.2f} km - {activity['time']:.2f} min"
            activity_listbox.insert(tk.END, entry)
        graphing()
        update_weekly_goal_progress()
        popup.destroy()

    submit_button = tk.Button(popup, text = "Submit", font = (FONT, 24), command = submit)
    submit_button.grid(row = 2, column = 0, padx = 20, pady = 10, sticky = "w")

def edit_profile() -> None: #Editing profile details
    popup2 = tk.Toplevel(root)
    popup2.title(f"Edit User Profile")
    popup2.geometry("700x250")

    tk.Label(popup2, text = "Select Which Field You Want to Edit:", font = (FONT, 20)).grid(row = 0, column = 0, padx = 10, pady = 10)

    options_var = tk.StringVar(value = "Name")
    field_options = ["Name", "Age", "Gender", "Weight", "Height"]

    dropdown = tk.OptionMenu(popup2, options_var, *field_options)
    dropdown.config(font = (FONT, 18), padx = 10, pady = 10)
    dropdown.grid(row = 0, column = 1)

    tk.Label(popup2, text = "Enter New Value:", font = (FONT, 20), padx = 10, pady = 10).grid(row = 1, column = 0)
    value_entry = tk.Entry(popup2, font = (FONT, 20))
    value_entry.grid(row = 1, column = 1, padx = 10, pady = 10)

    def submit_2() -> None: #Submitting function for profile details
        try:
            value = value_entry.get()
            field = options_var.get()
            garmin.update_settings(field, value)
            match field:
                case "Name":
                    name_label.config(text = f"Name: {garmin.name}")
                case "Age":
                    age_label.config(text = f"Age: {garmin.age}")
                case "Gender":
                    gender_label.config(text = f"Gender: {garmin.gender}")
                case "Height":
                    height_label.config(text = f"Height: {garmin.height:.1f} cm")
                    bmi_label.config(text = f"BMI: {garmin.bmi:.2f}")
                case "Weight":
                    weight_label.config(text = f"Weight: {garmin.weight:.1f} kg")
                    bmi_label.config(text = f"BMI: {garmin.bmi:.2f}")
            popup2.destroy()
        except:
            messagebox.showwarning("Invalid Input", "Choose a field and enter a valid value")

    submit_button = tk.Button(popup2, text = "Submit", font = (FONT, 20), command = submit_2)
    submit_button.grid(row = 2, column = 1, padx = 10, pady = 10)
            

root = tk.Tk()
root.title("Garmin Tracker App")
root.geometry("1440x900")
FONT = "Georgia"

'''
TITLE FRAME ROW 0 COLUMN 0
'''
#Title
title_frame = tk.Frame(root)
title_frame.grid(row = 0, column = 0, padx = (100, 20), pady = 10)

title = tk.Label(title_frame, text = "Garmin Tracker App", font = ("Impact", 75))
title.grid(row = 0, column = 0, padx = (20,5), pady = (20, 10), sticky = "w")

#Date and Time
date_label = tk.Label(title_frame, text = "", font = (FONT, 30))
date_label.grid(row = 1, column = 0, padx = 20, pady = (0, 20), sticky="w")

'''
GRAPH FRAME ROW 1 COLUMN 0
'''
#Graph Placeholder
graph_frame = tk.Frame(root)
graph_frame.grid(row = 1, column = 0, padx = (90, 10), sticky = "nsew")

'''
BUTTONS and SELECTION FRAME ROW 2 COLUMN 0
'''
#Activity Radiobuttons
activity_type = tk.StringVar(value = "Run")

radio_frame = tk.Frame(root)
radio_frame.grid(row = 2, column = 0, padx = (90, 20), pady = (20,40) , sticky = "n")
select_activity_label = tk.Label(radio_frame, text = "Select Activity to Add New or View All Time:", font = (FONT, 23))
select_activity_label.grid(row = 0, column = 0, columnspan = 4, pady = (0, 10), sticky = "w")

run_button = tk.Radiobutton(radio_frame, text = "Run", font = (FONT, 20), variable = activity_type, value = "Run")
run_button.grid(row = 1, column = 0, padx = 5)

swim_button = tk.Radiobutton(radio_frame, text = "Swim", font = (FONT, 20), variable = activity_type, value = "Swim")
swim_button.grid(row = 1, column = 1, padx = 5)

bike_button = tk.Radiobutton(radio_frame, text = "Bike", font = (FONT, 20), variable = activity_type, value = "Bike")
bike_button.grid(row = 1, column = 2, padx = 5)

#Actions
add_button = tk.Button(radio_frame, text = "Add Activity", font = (FONT, 17), width = 9, command = add_activity)
add_button.grid(row = 2, column = 0, padx = 5, pady = 5)

def save_all() -> None: #Save file to first_last.txt
    garmin.save_all()
    messagebox.showinfo("Success", f"Data saved to {garmin.name.replace(" ", "_")}.txt")

def load_file() -> None: #Load file using the users save name
    popup5 = tk.Toplevel(root)
    tk.Label(popup5, text = "Please Enter Your Save Name", font = (FONT, 17)).pack()
    entry_name = tk.Entry(popup5, font = (FONT, 17))
    entry_name.pack()

    def submit_load() -> None: 
        name = entry_name.get()
        garmin.load_file(name)
        activity_listbox.delete(0, tk.END)
        for activity in garmin.activities: 
            entry = f"{activity['date']} - {activity['type']} - {activity['distance']:.2f} km - {activity['time']:.2f} min"
            activity_listbox.insert(tk.END, entry)

        name_label.config(text = f"Name: {garmin.name}") 
        age_label.config(text = f"Age: {garmin.age}")
        gender_label.config(text = f"Gender: {garmin.gender}")
        height_label.config(text = f"Height: {garmin.height:.1f} cm")
        weight_label.config(text = f"Weight: {garmin.weight:.1f} kg")
        bmi_label.config(text = f"BMI: {garmin.bmi:.2f}")
        popup5.destroy()
        graphing()
        update_weekly_goal_progress()

    tk.Button(popup5, text = "Load", font = (FONT, 17), command = submit_load).pack(pady = 10)

save_button = tk.Button(radio_frame, text = "Save All", font = (FONT, 17), width = 9, command = save_all)
save_button.grid(row = 2, column = 2, padx = 5, pady = 5)

all_time_button = tk.Button(radio_frame, text = "All Time Stats", font = (FONT, 17), width = 9, command = display_all_time)
all_time_button.grid(row = 2, column = 1, padx = 5, pady = 5)

load_button = tk.Button(radio_frame, text = "Load File", font = (FONT, 17), width = 9, command = load_file)
load_button.grid(row = 2, column = 3, padx = 5, pady = 5)

'''
GENERAL STATISTICS ROW 0 COLUMN 1
'''
user_frame = tk.Frame(root, borderwidth = 1)
user_frame.grid(row = 0, column = 1, padx = (10, 90), pady = (30, 10) , sticky = "nsew")

top_bar = tk.Frame(user_frame)
top_bar.grid(row = 0, column = 0, columnspan = 3, sticky = "ew")

dots_button = tk.Button(top_bar, text = "⋮", font = (FONT, 25, "bold"), relief = "flat", cursor = "hand1", command = edit_profile)
dots_button.pack(side = "right", padx = 10, pady = 5)

stat_label = tk.Label(top_bar, text = "User Profile", font = (FONT, 25))
stat_label.pack(side = "left", padx = (10, 0), pady = 10)

name_label = tk.Label(user_frame, text = f"Name: {garmin.name}", font = (FONT, 19), width = 15)
name_label.grid(row = 1, column = 0, padx = 10, pady = 10)

height_label = tk.Label(user_frame, text = f"Height: {garmin.height} cm", font = (FONT, 19), width = 12)
height_label.grid(row = 1, column = 1, padx = 10, pady = 10)

weight_label = tk.Label(user_frame, text = f"Weight: {garmin.weight} kg", font = (FONT, 19), width = 12)
weight_label.grid(row = 1, column = 2, padx = 10, pady = 10)

gender_label = tk.Label(user_frame, text = f"Gender: {garmin.gender}", font = (FONT, 19), width = 15)
gender_label.grid(row = 2, column = 0, padx = 10, pady = 10)

age_label = tk.Label(user_frame, text = f"Age: {garmin.age}", font = (FONT, 19), width = 12)
age_label.grid(row = 2, column = 1, padx = 10, pady = 10)

bmi_label = tk.Label(user_frame, text = f"BMI: {garmin.bmi:.2f}", font = (FONT, 19), width = 12)
bmi_label.grid(row = 2, column = 2, padx = 10, pady = 10)

'''
ACTIVITY LOG ROW 1 COLUMN 1
'''
log_frame = tk.Frame(root, borderwidth = 1)
log_frame.grid(row = 1, column = 1, padx = (10, 90), pady = 5, sticky = "nsew")

log_label = tk.Label(log_frame, text = "Activity Log", font = (FONT, 25))
log_label.grid(row = 0, column = 0, sticky = "w", padx = (10, 30), pady = (10, 0))

info_label = tk.Label(log_frame, text = "Select Activities for More Information", font = (FONT, 20))
info_label.grid(row = 1, column = 0, sticky = "w", padx = (10, 30), pady = 10)

log_scrollbar = tk.Scrollbar(log_frame, orient = "vertical")
log_scrollbar.grid(row = 2, column = 1, sticky = "ns")

activity_listbox = tk.Listbox(log_frame, yscrollcommand = log_scrollbar.set, font = ("Courier", 20), width = 40, height = 14)
activity_listbox.grid(row = 2, column = 0, sticky = "nsew")
activity_listbox.bind("<<ListboxSelect>>", show_activity_details)

log_scrollbar.config(command = activity_listbox.yview)

'''
PROGRESS BAR ROW 2 COLUMN 1
'''
def update_weekly_goal_progress() -> None: #Update the weekly progress bar until the user reaches 150 mins
    today = datetime.now().date()
    last_7_days = [today - timedelta(days = i) for i in range(7)]
    total_minutes = 0
    for activity in garmin.activities:
        activity_date = datetime.strptime(activity["date"], "%Y-%m-%d").date()
        if activity_date in last_7_days:
            total_minutes += activity["time"]

    goal_progress['value'] = total_minutes
    if total_minutes < 150:
        goal_status.config(text = f"{int(total_minutes)} / 150 min")
    else:
        goal_status.config(text = f"Weekly Goal Completed!")

goal_frame = tk.Frame(root, borderwidth = 1)
goal_frame.grid(row = 2, column = 1, padx = (10, 90), pady = (0, 50), sticky = "nsew")

goal_title = tk.Label(goal_frame, text = "Weekly Goal: 150 Minutes of Activity", font = (FONT, 22))
goal_title.pack(pady = (10, 5))

goal_progress = ttk.Progressbar(goal_frame, orient = "horizontal", length = 400, mode = 'determinate', maximum = 150)
goal_progress.pack(pady = 5)

goal_status = tk.Label(goal_frame, text = "", font = (FONT, 18))
goal_status.pack(pady = 5)


if __name__ == "__main__":
    load_screen()
    update_datetime()
    graphing()
    update_weekly_goal_progress()
    root.mainloop()