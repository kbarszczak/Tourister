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
        master.geometry("800x800")
        master.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('default')

        # create a new frame to hold the RecorderGUI
        recorder_frame = ttk.Frame(master, padding=20)
        recorder_frame.pack()

        # create an instance of the RecorderGUI and pack it into the new frame
        self.recorder_gui = RecorderGUI(recorder_frame)

        self.button = ttk.Button(master, text="Recommend me route!", command=self.update_map)
        self.button.pack(pady=10)

        # create a new frame to hold the listbox
        list_frame = ttk.Frame(master, width=600, padding=20)
        list_frame.pack(fill=tk.BOTH, padx=10, pady=10)

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

    def update_map(self):
        text = self.recorder_gui.text
        places = get_places(text)[0:5]
        places_names = [place[1] for place in places]
        places_locations = [(place[3], place[4]) for place in places]
        self.places_listbox.delete(0, tk.END)
        for place in places_names:
            self.places_listbox.insert(tk.END, place)
        self.map_frame.update_map(places_locations)



root = tk.Tk()
root.configure(bg='#f0f0f0')
style = ttk.Style()
style.configure('Accent.TButton', background='#0080ff', foreground='#ffffff', font=('Arial', 12))
style.configure('Accent.TLabel', background='#f0f0f0', foreground='#333333', font=('Arial', 12))
gui = MainGUI(root)
root.mainloop()
