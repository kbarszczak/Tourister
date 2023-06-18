import tkinter as tk
from tkinter import ttk
from recorder_gui import RecorderGUI
from map_frame import MapFrame
from model import get_places

class MainGUI:

    def __init__(self, master):
        self.master = master
        self.tk = master
        master.title("Main Window")
        master.geometry("800x1000")
        master.configure(bg='#f0f0f0')
        self.places_names = []

        self.style = ttk.Style()
        self.style.theme_use('default')

        # create a new frame to hold the RecorderGUI
        recorder_frame = ttk.Frame(master, padding=20)
        recorder_frame.pack()

        # create an instance of the RecorderGUI and pack it into the new frame
        self.recorder_gui = RecorderGUI(recorder_frame)

        self.num_days_label = ttk.Label(master, text="Number of Days:")
        self.num_days_label.pack(pady=5)
        self.num_days_spinbox = ttk.Spinbox(master, from_=1, to=10)
        self.num_days_spinbox.insert(0, "1")
        self.num_days_spinbox.pack(pady=5)


        self.button = ttk.Button(master, text="Recommend me route!", command=self.update_map)
        self.button.pack(pady=5)

        # create a new frame to hold the listbox
        list_frame = ttk.Frame(master, width=600, padding=20)
        list_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # create a listbox and pack it into the new frame
        self.places_listbox = tk.Listbox(list_frame, height=7)
        self.places_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # create a scrollbar for the listbox
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.places_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.places_listbox.config(yscrollcommand=scrollbar.set)

        # Create the map frame
        self.map_frame = MapFrame(self)
        self.map_frame.pack(padx=10, pady=10)

        self.choose_day_spinbox = ttk.Spinbox(master, from_=1, to=1, state=tk.DISABLED, command=self.num_days_spinbox_callback)
        self.choose_day_spinbox.insert(0, "1")
        self.choose_day_spinbox.pack()


    def update_map(self):
        text = self.recorder_gui.text
        num_places = int(self.num_days_spinbox.get()) * 5
        places = get_places(text)[0:num_places]
        self.places_names = [place[1] for place in places]
        places_locations = [(place[3], place[4]) for place in places]
        self.update_route(0)
        self.update_day_spinbox()
        self.map_frame.create_routes(places_locations)

    def update_day_spinbox(self):
        num_days = int(self.num_days_spinbox.get())
        self.choose_day_spinbox.config(from_=1, to=num_days, state=tk.NORMAL)
        self.choose_day_spinbox.delete(0, tk.END)
        self.choose_day_spinbox.insert(0, '1')

    def num_days_spinbox_callback(self):
        chosen_day = int(self.choose_day_spinbox.get()) - 1 
        self.map_frame.change_day(chosen_day)
        self.update_route(chosen_day)

    def update_route(self, chosen_day):
        self.places_listbox.delete(0, tk.END)
        for place in self.places_names[chosen_day*5:chosen_day*5+5]:
            self.places_listbox.insert(tk.END, place)
        



root = tk.Tk()
root.configure(bg='#f0f0f0')
style = ttk.Style()
style.configure('Accent.TButton', background='#0080ff', foreground='#ffffff', font=('Arial', 12))
style.configure('Accent.TLabel', background='#f0f0f0', foreground='#333333', font=('Arial', 12))
gui = MainGUI(root)
root.mainloop()
