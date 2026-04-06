import tkinter as tk
from tkintermapview import TkinterMapView
from pyowm import OWM
API_KEY = "903c7b602f35c53a208eac1477998b99"
owm = OWM(API_KEY)
root = tk.Tk()
root.configure(bg="#00008B")
root.attributes("-fullscreen", True)
root.title("Weatherly")
root.iconbitmap("Images/icon.ico")
map_widget = TkinterMapView(root, width=800, height=600, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# Set default position (London) and zoom level
map_widget.set_position(51.5074, -0.1278) 
map_widget.set_zoom(5)
root.mainloop()