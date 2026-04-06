import tkinter as tk
from pyowm import OWM
from PIL import Image, ImageTk
import requests

# --- SETUP ---
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
            
            # 1. Place it
            suggestion_list.place(anchor="n", relx=0.5, rely=0.59)
            
            # 2. BRING TO FRONT: This stops the Quit button from overriding the list
            suggestion_list.lift()
            user_input.lift() # Also lift the search bar just in case
        else:
            suggestion_list.place_forget()
    except:
        pass

def clear_placeholder(event):
    if user_input.get() == "Search city...":
        user_input.delete(0, tk.END)
    
    # Lift the search bar when the user clicks into it
    user_input.lift()

def on_city_select(event):
    selection = suggestion_list.curselection()
    if selection:
        index = selection[0]
        city_data = current_search_results[index]
        
        full_name = f"{city_data['name']}, {city_data['country']}"
        user_input.delete(0, tk.END)
        user_input.insert(0, full_name)
        
        suggestion_list.place_forget()
        print(f"Coordinates: {city_data['lat']}, {city_data['lon']}")



# --- UI ELEMENTS ---

menu_frame = tk.Frame(root, bg=bg_color)
menu_frame.pack(fill="both", expand=True)

# Logo
logo_image = Image.open(r"Images/Logo.png")
w_logo, h_logo = logo_image.size
tk_logo = ImageTk.PhotoImage(logo_image.resize((int(w_logo * 0.6), int(h_logo * 0.6))))

image_label = tk.Label(menu_frame, image=tk_logo, bg=bg_color)
image_label.image = tk_logo
image_label.place(anchor="center", relx=0.5, rely=0.35)

# Search Input
user_input = tk.Entry(menu_frame, font=("Arial", 28), width=40, borderwidth=0)
user_input.insert(0, "Search city...")
user_input.place(anchor="center", relx=0.5, rely=0.55)
user_input.lift()

# Suggestion Listbox
suggestion_list = tk.Listbox(menu_frame, font=("Arial", 18), width=61, 
                             height=5, borderwidth=0, highlightthickness=0)

# Quit Button
# Resizing it to 60x60 so it's a clear icon but not overwhelming
quit_raw = Image.open(r"Images/Quit.png")
tk_quit = ImageTk.PhotoImage(quit_raw)

quit_button = tk.Button(
    menu_frame, 
    image=tk_quit, 
    command=root.destroy, 
    bg=bg_color, 
    activebackground=bg_color, 
    borderwidth=0, 
    highlightthickness=0
)
quit_button.image = tk_quit
# Placed at rely=0.9 to keep it at the very bottom, away from the search bar
quit_button.place(relx=0.5, rely=0.85, anchor="center")

# Bindings
user_input.bind("<FocusIn>", clear_placeholder)
user_input.bind("<KeyRelease>", get_suggestions)
user_input.lift()
suggestion_list.bind("<<ListboxSelect>>", on_city_select)

root.mainloop()