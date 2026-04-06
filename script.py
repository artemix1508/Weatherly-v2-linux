import tkinter as tk
from pyowm import OWM
from PIL import Image, ImageTk

API_KEY = "903c7b602f35c53a208eac1477998b99"
owm = OWM(API_KEY)

root = tk.Tk()
bg_color = "#42a5f5"
root.configure(bg=bg_color)
root.attributes("-fullscreen", True)
root.title("Weatherly")


menu_frame = tk.Frame(root, bg=bg_color)
menu_frame.pack(fill="both", expand=True)

logo_image = Image.open(r"Images/Logo.png")
width, height = logo_image.size
new_width = int(width * 0.6)
new_height = int(height * 0.6)
tk_img = ImageTk.PhotoImage(logo_image.resize((new_width, new_height)))

image_label = tk.Label(menu_frame, image=tk_img, bg=bg_color)
image_label.image = tk_img 
image_label.pack()
image_label.place(anchor="center", relx=0.5, rely=0.35)

user_input = tk.Entry(root, font=("Arial", 28), width=50, borderwidth=0)
user_input.pack()
user_input.place(anchor="center", relx=0.5, rely=0.55)
user_input.insert(0, "Search city...")
def clear_placeholder(event):
    if user_input.get() == "Search city...":
        user_input.delete(0, tk.END)

user_input.bind("<FocusIn>", clear_placeholder)

root.mainloop()
