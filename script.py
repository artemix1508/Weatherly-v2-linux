import tkinter as tk
from pyowm import OWM
from PIL import Image, ImageTk
import requests

API_KEY = "903c7b602f35c53a208eac1477998b99"
owm = OWM(API_KEY)

root = tk.Tk()
bg_color = "#42a5f5"
root.configure(bg=bg_color)
root.attributes("-fullscreen", True)
root.title("Weatherly")

current_search_results = []

# --- FUNCTIONS ---

def get_suggestions(event):
    query = user_input.get()
    if query == "Search city..." or len(query) < 3:
        suggestion_list.place_forget()
        return

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={API_KEY}"
    try:
        response = requests.get(url)
        cities = response.json()
        if cities:
            suggestion_list.delete(0, tk.END)
            global current_search_results
            current_search_results = cities
            for city in cities:
                display = f"{city['name']}, {city.get('state', '')} {city['country']}".replace(" ,", ",")
                suggestion_list.insert(tk.END, display)
            
            suggestion_list.place(anchor="n", relx=0.5, rely=0.59)
            suggestion_list.lift() 
        else:
            suggestion_list.place_forget()
    except:
        pass

def on_city_select(event):
    selection = suggestion_list.curselection()
    if selection:
        index = selection[0]
        city_data = current_search_results[index]
        user_input.delete(0, tk.END)
        user_input.insert(0, f"{city_data['name']}, {city_data['country']}")
        suggestion_list.place_forget()

def clear_placeholder(event):
    if user_input.get() == "Search city...":
        user_input.delete(0, tk.END)

def settings_opened():
    menu_frame.place_forget()
    settings_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    root.update_idletasks() # Force redraw to apply background color first
    settings_back_button.lift()

def settings_closed():
    settings_frame.place_forget()
    menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# --- UI SETUP ---

menu_frame = tk.Frame(root, bg=bg_color)
menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

settings_frame = tk.Frame(root, bg=bg_color)

# --- IMPROVED IMAGE LOADING ---
def load_img(path, size_mult):
    img = Image.open(path).convert("RGBA") # Force RGBA for transparency
    w, h = img.size
    new_size = (int(w * size_mult), int(h * size_mult))
    # Resize using Image.LANCZOS to keep the alpha channel clean
    img = img.resize(new_size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Pre-load all images
tk_logo = load_img(r"Images/Logo.png", 0.6)
tk_quit = load_img(r"Images/Quit.png", 0.35)
tk_settings = load_img(r"Images/Settings.png", 0.35)
tk_back = load_img(r"Images/back.png", 0.35)

# --- MENU WIDGETS ---
logo_lbl = tk.Label(menu_frame, image=tk_logo, bg=bg_color)
logo_lbl.image = tk_logo
logo_lbl.place(anchor="center", relx=0.5, rely=0.35)

user_input = tk.Entry(menu_frame, font=("Arial", 28), width=40, borderwidth=0)
user_input.insert(0, "Search city...")
user_input.place(anchor="center", relx=0.5, rely=0.55)

suggestion_list = tk.Listbox(menu_frame, font=("Arial", 18), width=61, height=5, borderwidth=0, highlightthickness=0)

settings_btn = tk.Button(menu_frame, image=tk_settings, bg=bg_color, activebackground=bg_color, 
                         borderwidth=0, highlightthickness=0, command=settings_opened)
settings_btn.image = tk_settings
settings_btn.place(relx=0.5, rely=0.82, anchor="center")

quit_btn = tk.Button(menu_frame, image=tk_quit, bg=bg_color, activebackground=bg_color, 
                     borderwidth=0, highlightthickness=0, command=root.destroy)
quit_btn.image = tk_quit
quit_btn.place(relx=0.5, rely=0.92, anchor="center")

# --- SETTINGS WIDGETS ---
settings_back_button = tk.Button(
    settings_frame, 
    image=tk_back,
    command=settings_closed,
    bg=bg_color,
    activebackground=bg_color,
    borderwidth=0, 
    highlightthickness=0
)
settings_label = tk.Label(settings_frame,
    image=tk_settings,
    bg=bg_color,
    activebackground=bg_color,
    borderwidth=0, 
    highlightthickness=0
)
settings_label.image = tk_settings
settings_label.place(relx=0.5, rely=0.2, anchor="center")

settings_back_button.image = tk_back
settings_back_button.place(relx=0.5, rely=0.85, anchor="center")

# --- BINDINGS ---
user_input.bind("<FocusIn>", clear_placeholder)
user_input.bind("<KeyRelease>", get_suggestions)
suggestion_list.bind("<<ListboxSelect>>", on_city_select)

root.mainloop()