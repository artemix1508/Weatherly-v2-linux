import tkinter as tk
from pyowm import OWM
from PIL import Image, ImageTk
import requests, json
import os

API_KEY = "903c7b602f35c53a208eac1477998b99"
owm = OWM(API_KEY)
metric_selected = ""

if os.path.exists("data.json"):
    with open("data.json", "r") as file:
        try:
            metric_selected = json.load(file).get("metric", "celcius")
        except:
            metric_selected = "celcius"
else:
    metric_selected = "celcius"

root = tk.Tk()
bg_color = "#42a5f5"
root.configure(bg=bg_color)
root.attributes("-fullscreen", True)
root.title("Weatherly")

current_search_results = []

def load_img(path, fixed_height):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    aspect_ratio = w / h
    new_h = int(fixed_height)
    new_w = int(new_h * aspect_ratio)
    resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_img)
button_h = 60
def update_button_image(button_obj, image_path):
    try:
        new_tk_img = load_img(image_path, button_h)
        button_obj.config(image=new_tk_img)
        button_obj.image = new_tk_img
    except Exception as e:
        print(f"Update Error: {e}")

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

def select_metric(metric):
    global metric_selected
    metric_selected = metric
    with open("data.json", "w") as file:
        json.dump({"metric": metric_selected}, file)
    
    update_button_image(celcius_button, "Images/Celsius.png")
    update_button_image(fahrenheit_button, "Images/Fahrenheit.png")
    update_button_image(kelvin_button, "Images/Kelvin.png")
    
    if metric == "celcius":
        update_button_image(celcius_button, "Images/CelsiusFocused.png")
    elif metric == "fahrenheit":
        update_button_image(fahrenheit_button, "Images/FahrenheitFocused.png")
    elif metric == "kelvin":
        update_button_image(kelvin_button, "Images/KelvinFocused.png")

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
    root.update_idletasks()
    settings_back_button.lift()

def settings_closed():
    settings_frame.place_forget()
    menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

menu_frame = tk.Frame(root, bg=bg_color)
menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
settings_frame = tk.Frame(root, bg=bg_color)

tk_logo = load_img(r"Images/Logo.png", 400)
tk_quit = load_img(r"Images/Quit.png", 60)
tk_settings = load_img(r"Images/Settings.png", 60)
tk_back = load_img(r"Images/back.png", 60)
tk_search = load_img(r"Images/search.png", 150)
tk_metrics = load_img(r"Images/Metrics.png", 50)

tk_celsius = load_img(r"Images/Celsius.png", button_h)
tk_fahrenheit = load_img(r"Images/Fahrenheit.png", button_h)
tk_kelvin = load_img(r"Images/Kelvin.png", button_h)

logo_lbl = tk.Label(menu_frame, image=tk_logo, bg=bg_color)
logo_lbl.image = tk_logo
logo_lbl.place(anchor="center", relx=0.5, rely=0.35)

user_input = tk.Entry(menu_frame, font=("Arial", 28), width=40, borderwidth=0)
user_input.insert(0, "Search city...")
user_input.place(anchor="center", relx=0.5, rely=0.55)

suggestion_list = tk.Listbox(menu_frame, font=("Arial", 18), width=61, height=5, borderwidth=0, highlightthickness=0)

settings_btn = tk.Button(menu_frame, image=tk_settings, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0, command=settings_opened)
settings_btn.image = tk_settings
settings_btn.place(relx=0.5, rely=0.82, anchor="center")

quit_btn = tk.Button(menu_frame, image=tk_quit, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0, command=root.destroy)
quit_btn.image = tk_quit
quit_btn.place(relx=0.5, rely=0.92, anchor="center")

settings_back_button = tk.Button(settings_frame, image=tk_back, command=settings_closed, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0)
search_button = tk.Button(menu_frame, image=tk_search, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0)
search_button.image = tk_search
search_button.place(relx=0.8, rely=0.55, anchor="center")

settings_label = tk.Label(settings_frame, image=tk_settings, bg=bg_color, borderwidth=0)
metrics_label = tk.Label(settings_frame, image=tk_metrics, bg=bg_color, borderwidth=0)
metrics_label.place(relx=0.5, rely=0.15, anchor="center")
fahrenheit_button = tk.Button(settings_frame, image=tk_fahrenheit, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0, command=lambda: select_metric("fahrenheit"))
fahrenheit_button.place(relx=0.5, rely=0.25, anchor="center")

celcius_button = tk.Button(settings_frame, image=tk_celsius, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0, command=lambda: select_metric("celcius"))
celcius_button.place(relx=0.5, rely=0.325, anchor="center")

kelvin_button = tk.Button(settings_frame, image=tk_kelvin, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0, command=lambda: select_metric("kelvin"))
kelvin_button.place(relx=0.5, rely=0.4, anchor="center")

settings_label.image = tk_settings
settings_label.place(relx=0.5, rely=0.05, anchor="center")
settings_back_button.image = tk_back
settings_back_button.place(relx=0.5, rely=0.85, anchor="center")

user_input.bind("<FocusIn>", clear_placeholder)
user_input.bind("<KeyRelease>", get_suggestions)
suggestion_list.bind("<<ListboxSelect>>", on_city_select)
root.bind("<Escape>", lambda e: root.destroy())

root.after(100, lambda: select_metric(metric_selected))

root.mainloop()